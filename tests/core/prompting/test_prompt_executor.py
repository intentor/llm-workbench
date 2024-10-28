"""Tests for SelectorResponseGenerator."""

from unittest.mock import patch
import pytest

from core.prompting.executor import PromptExecutor

PROMPT_TEXT: str = 'Prompt text'


@pytest.fixture
def prompt_model() -> str:
    return PROMPT_TEXT


@pytest.fixture
def prompt_context() -> str:
    return '/context ' + PROMPT_TEXT


@pytest.fixture
def prompt_endpoint() -> str:
    return '/endpoint http://localhost:3000/data/1'


@pytest.fixture
def history():
    with patch('core.prompting.history.PromptHistory') as mock_class:
        instance = mock_class.return_value
        yield instance


@pytest.fixture
def generator_model():
    with patch('core.prompting.base.ResponseGenerator') as mock_class:
        instance = mock_class.return_value
        instance.get_type.return_value = 'model'
        instance.generate.return_value = 'model'
        yield instance


@pytest.fixture
def generator_context():
    with patch('core.prompting.base.ResponseGenerator') as mock_class:
        instance = mock_class.return_value
        instance.get_type.return_value = 'context'
        instance.generate.return_value = 'context'
        yield instance


@pytest.fixture
def generator_endpoint():
    with patch('core.prompting.base.ResponseGenerator') as mock_class:
        instance = mock_class.return_value
        instance.get_type.return_value = 'endpoint'
        instance.generate.return_value = 'endpoint'
        yield instance


@pytest.fixture
def generators(generator_model, generator_context, generator_endpoint):
    return [
        generator_model,
        generator_context,
        generator_endpoint
    ]


def test_no_generators(history, prompt_model):
    prompt_executor = PromptExecutor(history, {})

    with pytest.raises(ValueError):
        prompt_executor.execute(prompt_model)


def test_unavailable_generator(
        history,
        generator_context,
        prompt_model
):
    prompt_executor = PromptExecutor(history, [generator_context])

    with pytest.raises(ValueError):
        prompt_executor.execute(prompt_model)


def test_generator_model(
        history,
        generators,
        prompt_model
):
    prompt_executor = PromptExecutor(history, generators)

    response = prompt_executor.execute(prompt_model)

    assert response == 'model'


def test_generator_context(
        history,
        generators,
        prompt_context
):
    prompt_executor = PromptExecutor(history, generators)

    response = prompt_executor.execute(prompt_context)

    assert response == 'context'


def test_generator_endpoint(
        history,
        generators,
        prompt_endpoint
):
    prompt_executor = PromptExecutor(history, generators)

    response = prompt_executor.execute(prompt_endpoint)

    assert response == 'endpoint'
