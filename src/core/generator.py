"""Execute prompts in a given response generator."""

from abc import abstractmethod
from logging import getLogger
import json
import requests

import jinja2
from ollama import Client

from core.indexer import ContextIndexer
from core.prompt import (
    GeneratedResponse,
    Prompt,
    PromptHistory,
    PromptHistoryEntry,
    PromptPatternReplacer,
    PromptType
)

logger = getLogger()


class ResponseGenerator():
    """Generate responses based on a prompt."""

    @abstractmethod
    def generate(self, prompt: Prompt) -> GeneratedResponse:
        """Generates a respons based on a prompt.

        Args:
            - text: Prompt to generate a response.

        Returns:
            Response from the generation.
        """
        raise NotImplementedError()


class HistoryAwareResponseGeneator(ResponseGenerator):
    """Generate responses based on a prompt, with access to prompt history and 
    prompt pattern replacement."""

    def __init__(self, history: PromptHistory):
        """
        Args:
            - history: Prompt history manager.
        """
        self._history = history
        self._replacer = PromptPatternReplacer(history)

    @abstractmethod
    def generate(self, prompt: Prompt) -> GeneratedResponse:
        raise NotImplementedError()

    def _append_history(self, prompt: Prompt, response: GeneratedResponse):
        self._history.append(PromptHistoryEntry(
            label=prompt.get_label(),
            prompt=prompt.get_original_prompt(),
            response=response
        ))


class ContextResponseGenerator(HistoryAwareResponseGeneator):
    """Generate responses from indexed context."""

    def __init__(
        self,
            history: PromptHistory,
            indexer: ContextIndexer
    ):
        """
        Args:
            - history: Prompt history manager.
            - indexer: Index manager
        """
        super().__init__(history)
        self._indexer = indexer

    def generate(self, prompt: Prompt) -> GeneratedResponse:
        prompt_text = self._replacer.replace(prompt.get_prompt())
        response = self._indexer.query(
            prompt_text,
            prompt.get_top_k(),
            prompt.get_file_name())

        generated_response = GeneratedResponse(
            value=response

        )
        self._append_history(prompt, generated_response)

        logger.debug('m=generate type=context prompt=%s response=%s',
                     prompt_text, generated_response)

        return generated_response


class EndpointResponseGenerator(HistoryAwareResponseGeneator):
    """Generate responses from endpoints."""

    def generate(self, prompt: Prompt) -> GeneratedResponse:
        url = prompt.get_prompt()

        response = requests.get(url, timeout=10)
        contents = response.text

        generated_response = GeneratedResponse(
            value=contents
        )
        self._append_history(prompt, generated_response)

        logger.debug('m=generate type=endpoint url=%s response=%s',
                     url, generated_response)

        return generated_response


class EchoResponseGenerator(HistoryAwareResponseGeneator):
    """Echo the prompt."""

    def generate(self, prompt: Prompt) -> str:
        response = self._replacer.replace(prompt.get_prompt())

        generated_response = GeneratedResponse(
            value=response
        )
        self._append_history(prompt, generated_response)

        logger.debug('m=generate type=echo response=%s', generated_response)

        return generated_response


class TemplateResponseGenerator(HistoryAwareResponseGeneator):
    """Apply the last response as JSON in a template defined by the prompt.."""

    def generate(self, prompt: Prompt) -> GeneratedResponse:
        template_format = self._replacer.replace(prompt.get_prompt())

        try:
            last_response = self._history.get_last_response()
            data = json.loads(last_response)
            context = {"context": data}

            environment = jinja2.Environment(
                extensions=['jinja2_iso8601.ISO8601Extension'])
            template = environment.from_string(template_format)
            response = template.render(context)
        except Exception as e:
            logger.error('m=generate type=template  e=%s', e)
            response = ('Could not apply the last response to the template. '
                        'Please check the previous response and try again.')

        generated_response = GeneratedResponse(
            value=response
        )
        self._append_history(prompt, generated_response)

        logger.debug('m=generate type=template response=%s',
                     generated_response)

        return generated_response


class OllamaResponseGenerator(HistoryAwareResponseGeneator):
    """Generate responses from an LLM using Ollama."""

    def __init__(
        self,
            history: PromptHistory,
            ollama: Client,
            model_name: str = 'llama3'
    ):
        """
        Args:
            - history: Prompt history manager.
            - ollama: Client to access Ollama.
            - model_name: Name of the LLM model used for generation.
        """
        super().__init__(history)
        self._ollama = ollama
        self._model_name = model_name

    def generate(self, prompt: Prompt) -> GeneratedResponse:
        prompt_text = self._replacer.replace(prompt.get_prompt())
        ollama_response = self._ollama.generate(self._model_name, prompt_text)
        response = ollama_response['response']

        generated_response = GeneratedResponse(
            value=response,
            input_tokens=ollama_response['prompt_eval_count'],
            output_tokens=ollama_response['eval_count']
        )
        self._append_history(prompt, generated_response)

        logger.debug('m=generate type=ollama prompt=%s response=%s',
                     prompt_text, generated_response)

        return generated_response


class PromptTypeResponseGenerator(ResponseGenerator):
    """Generate responses based on prompt types."""

    def __init__(
        self,
        generators: dict[PromptType, ResponseGenerator]
    ):
        """
        Args:
            - generators: Generators to use per PromptType.
        """
        self._generators = generators

    def generate(self, prompt: Prompt) -> GeneratedResponse:
        prompt_type = prompt.get_prompt_type()

        if prompt_type in self._generators:
            return self._generators[prompt_type].generate(prompt)
        else:
            raise ValueError(
                f"Generator not available for prompt type {prompt_type}")
