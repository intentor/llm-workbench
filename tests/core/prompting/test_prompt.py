"""Tests for Prompt class."""

import pytest

from core.prompting.prompt import Prompt


@pytest.mark.parametrize(
    'prompt,label,tool_name,tool_parameters,actual_prompt', [
        (
            'Prompt text',
            '',
            '',
            {},
            'Prompt text'
        ),
        (
            '/toolname',
            '',
            'toolname',
            {},
            ''
        ),
        (
            '/toolname?param1=value_test1',
            '',
            'toolname',
            {'param1': 'value_test1'},
            ''
        ),
        (
            '/toolname?param1=value_test1&param2=value-test2',
            '',
            'toolname',
            {'param1': 'value_test1', 'param2': 'value-test2'},
            ''
        ),
        (
            '/toolname Prompt text',
            '',
            'toolname',
            {},
            'Prompt text'
        ),
        (
            '/toolname?param1=value_test1 Prompt text',
            '',
            'toolname',
            {'param1': 'value_test1'},
            'Prompt text'
        ),
        (
            '/toolname?param1=value_test1&param2=value-test2 Prompt text',
            '',
            'toolname',
            {'param1': 'value_test1', 'param2': 'value-test2'},
            'Prompt text'
        ),
        (
            ':lbl-test1 Prompt text',
            'lbl-test1',
            '',
            {},
            'Prompt text'
        ),
        (
            ':lbl-test1 /toolname',
            'lbl-test1',
            'toolname',
            {},
            ''
        ),
        (
            ':lbl-test1 /toolname?param1=value_test1',
            'lbl-test1',
            'toolname',
            {'param1': 'value_test1'},
            ''
        ),
        (
            ':lbl-test1 /toolname?param1=value_test1&param2=value-test2',
            'lbl-test1',
            'toolname',
            {'param1': 'value_test1', 'param2': 'value-test2'},
            ''
        ),
        (
            ':lbl-test1 /toolname Prompt text',
            'lbl-test1',
            'toolname',
            {},
            'Prompt text'
        ),
        (
            ':lbl-test1 /toolname?param1=value_test1 Prompt text',
            'lbl-test1',
            'toolname',
            {'param1': 'value_test1'},
            'Prompt text'
        ),
        (
            ':lbl-test1 /toolname?param1=value_test1&param2=value-test2 Prompt text',
            'lbl-test1',
            'toolname',
            {'param1': 'value_test1', 'param2': 'value-test2'},
            'Prompt text'
        )
    ]
)
def test_prompt_processing(
        prompt,
        label,
        tool_name,
        tool_parameters,
        actual_prompt):
    prompt_processor = Prompt(prompt)

    assert prompt_processor.get_original_prompt() == prompt
    assert str(prompt_processor) == prompt
    assert prompt_processor.get_label() == label
    assert prompt_processor.get_tool_name() == tool_name
    assert prompt_processor.get_prompt() == actual_prompt
    assert prompt_processor.get_tool_parameters() == tool_parameters
