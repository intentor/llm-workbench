"""Tests for SelectorResponseGenerator."""

from unittest.mock import patch
import pytest

from core.prompting.generator.selector import SelectorResponseGenerator
from core.prompting.base import Prompt

PROMPT_TEXT: str = 'Prompt text'


@pytest.fixture
def prompt_gateway() -> Prompt:
    return Prompt(PROMPT_TEXT)


@pytest.fixture
def prompt_context() -> Prompt:
    return Prompt('/context ' + PROMPT_TEXT)


@pytest.fixture
def prompt_endpoint() -> Prompt:
    return Prompt('/endpoint?url=http://localhost:3000/data/1')


@pytest.fixture
def generator_gateway():
    with patch('core.prompting.base.ResponseGenerator') as mock_class:
        instance = mock_class.return_value
        instance.get_type.return_value = 'gateway'
        instance.generate.return_value = 'gateway'
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
def generators(generator_gateway, generator_context, generator_endpoint):
    return [
        generator_gateway,
        generator_context,
        generator_endpoint
    ]


def test_no_generators(prompt_gateway):
    selector_generator = SelectorResponseGenerator({})

    with pytest.raises(ValueError):
        selector_generator.generate(prompt_gateway)


def test_unavailable_generator(
        generator_context,
        prompt_gateway
):
    selector_generator = SelectorResponseGenerator([generator_context])

    with pytest.raises(ValueError):
        selector_generator.generate(prompt_gateway)


def test_generator_gateway(
        generators,
        prompt_gateway
):
    selector_generator = SelectorResponseGenerator(generators)

    response = selector_generator.generate(prompt_gateway)

    assert response == 'gateway'


def test_generator_context(
        generators,
        prompt_context
):
    selector_generator = SelectorResponseGenerator(generators)

    response = selector_generator.generate(prompt_context)

    assert response == 'context'


def test_generator_endpoint(
        generators,
        prompt_endpoint
):
    selector_generator = SelectorResponseGenerator(generators)

    response = selector_generator.generate(prompt_endpoint)

    assert response == 'endpoint'
