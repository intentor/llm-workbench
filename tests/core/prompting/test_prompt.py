"""Tests for Prompt class."""

import pytest

from core.prompting.base import Prompt, DEFULT_GENERATOR_TYPE


@pytest.mark.parametrize(
    'prompt,label,generator_type,generator_parameters,actual_prompt', [
        (
            'Prompt text',
            '',
            DEFULT_GENERATOR_TYPE,
            {},
            'Prompt text'
        ),
        (
            '/generatortype',
            '',
            'generatortype',
            {},
            ''
        ),
        (
            '/generatortype?param1=value_test.1',
            '',
            'generatortype',
            {'param1': 'value_test.1'},
            ''
        ),
        (
            '/generatortype?param1=value_test.1&param2=value-test2',
            '',
            'generatortype',
            {'param1': 'value_test.1', 'param2': 'value-test2'},
            ''
        ),
        (
            '/generatortype Prompt text',
            '',
            'generatortype',
            {},
            'Prompt text'
        ),
        (
            '/generatortype?param1=value_test.1 Prompt text',
            '',
            'generatortype',
            {'param1': 'value_test.1'},
            'Prompt text'
        ),
        (
            '/generatortype?param1=value_test.1&param2=value-test2 Prompt text',
            '',
            'generatortype',
            {'param1': 'value_test.1', 'param2': 'value-test2'},
            'Prompt text'
        ),
        (
            ':lbl-test1 Prompt text',
            'lbl-test1',
            DEFULT_GENERATOR_TYPE,
            {},
            'Prompt text'
        ),
        (
            ':lbl-test1 /generatortype',
            'lbl-test1',
            'generatortype',
            {},
            ''
        ),
        (
            ':lbl-test1 /generatortype?param1=value_test.1',
            'lbl-test1',
            'generatortype',
            {'param1': 'value_test.1'},
            ''
        ),
        (
            ':lbl-test1 /generatortype?param1=value_test.1&param2=value-test2',
            'lbl-test1',
            'generatortype',
            {'param1': 'value_test.1', 'param2': 'value-test2'},
            ''
        ),
        (
            ':lbl-test1 /generatortype Prompt text',
            'lbl-test1',
            'generatortype',
            {},
            'Prompt text'
        ),
        (
            ':lbl-test1 /generatortype?param1=value_test.1 Prompt text',
            'lbl-test1',
            'generatortype',
            {'param1': 'value_test.1'},
            'Prompt text'
        ),
        (
            ':lbl-test1 /generatortype?param1=value_test.1&param2=value-test2 Prompt text',
            'lbl-test1',
            'generatortype',
            {'param1': 'value_test.1', 'param2': 'value-test2'},
            'Prompt text'
        )
    ]
)
def test_prompt_processing(
        prompt,
        label,
        generator_type,
        generator_parameters,
        actual_prompt):
    prompt_processor = Prompt(prompt)

    assert prompt_processor.get_original_prompt() == prompt
    assert str(prompt_processor) == prompt
    assert prompt_processor.get_label() == label
    assert prompt_processor.get_generator_type() == generator_type
    assert prompt_processor.get_prompt() == actual_prompt
    assert prompt_processor.get_generator_parameters() == generator_parameters
