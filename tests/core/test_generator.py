"""Tests for generator module."""

from unittest.mock import patch
import pytest

from core.generator import PromptTypeResponseGenerator
from core.prompt import Prompt, PromptType

PROMPT_TEXT: str = 'Prompt text'


@pytest.fixture
def prompt_generate() -> Prompt:
    return Prompt(PROMPT_TEXT)


@pytest.fixture
def prompt_context() -> Prompt:
    return Prompt('/context ' + PROMPT_TEXT)


@pytest.fixture
def generator_generate():
    with patch('core.generator.ResponseGenerator') as mock_class:
        instance = mock_class.return_value
        instance.generate.return_value = 'generate'
        yield instance


@pytest.fixture
def generator_context():
    with patch('core.generator.ResponseGenerator') as mock_class:
        instance = mock_class.return_value
        instance.generate.return_value = 'context'
        yield instance


@pytest.fixture
def generators(generator_generate, generator_context):
    return {
        PromptType.GENERATE: generator_generate,
        PromptType.CONTEXT: generator_context
    }


def test_prompt_type_generator_no_generators(prompt_generate):
    prompt_type_generator = PromptTypeResponseGenerator({})

    with pytest.raises(ValueError):
        prompt_type_generator.generate(prompt_generate)


def test_prompt_type_generator_unavailable_generator(
        generator_context,
        prompt_generate
):
    prompt_type_generator = PromptTypeResponseGenerator(
        {PromptType.CONTEXT: generator_context}
    )

    with pytest.raises(ValueError):
        prompt_type_generator.generate(prompt_generate)


def test_prompt_type_generator_generate(
        generators,
        prompt_generate
):

    prompt_type_generator = PromptTypeResponseGenerator(generators)

    response = prompt_type_generator.generate(prompt_generate)

    assert response == 'generate'


def test_prompt_type_generator_context(
        generators,
        prompt_context
):

    prompt_type_generator = PromptTypeResponseGenerator(generators)

    response = prompt_type_generator.generate(prompt_context)

    assert response == 'context'
