"""Tests for Prompt class."""

import pytest

from core.prompt import DEFAULT_SIMILARITY_TOP_K, Prompt, PromptType


@pytest.mark.parametrize(
    'prompt,label,top_k,file_name,prompt_type,actual_prompt', [
        (
            'Prompt',
            '',
            DEFAULT_SIMILARITY_TOP_K,
            '',
            PromptType.GENERATE,
            'Prompt'
        ),
        (
            'Prompt one',
            '',
            DEFAULT_SIMILARITY_TOP_K,
            '',
            PromptType.GENERATE,
            'Prompt one'
        ),
        (
            'Prompt one two',
            '',
            DEFAULT_SIMILARITY_TOP_K,
            '',
            PromptType.GENERATE,
            'Prompt one two'
        ),
        (
            'Multline\nprompt',
            '',
            DEFAULT_SIMILARITY_TOP_K,
            '',
            PromptType.GENERATE,
            'Multline\nprompt'
        ),
        (
            '/context Prompt',
            '',
            DEFAULT_SIMILARITY_TOP_K,
            '',
            PromptType.CONTEXT,
            'Prompt'
        ),
        (
            '/context Prompt one',
            '',
            DEFAULT_SIMILARITY_TOP_K,
            '',
            PromptType.CONTEXT,
            'Prompt one'
        ),
        (
            '/context Prompt one two',
            '',
            DEFAULT_SIMILARITY_TOP_K,
            '',
            PromptType.CONTEXT,
            'Prompt one two'
        ),
        (
            '/context Multline\nprompt',
            '',
            DEFAULT_SIMILARITY_TOP_K,
            '',
            PromptType.CONTEXT,
            'Multline\nprompt'
        ),
        (
            '/context:1 Prompt',
            '',
            1,
            '',
            PromptType.CONTEXT,
            'Prompt'
        ),
        (
            '/context:11 Prompt one',
            '',
            11,
            '',
            PromptType.CONTEXT,
            'Prompt one'
        ),
        (
            '/context:111 Prompt one two',
            '',
            111,
            '',
            PromptType.CONTEXT,
            'Prompt one two'
        ),
        (
            '/context:1111 Multline\nprompt',
            '',
            1111,
            '',
            PromptType.CONTEXT,
            'Multline\nprompt'
        ),
        (
            '/context?file="file.pdf" Prompt',
            '',
            DEFAULT_SIMILARITY_TOP_K,
            'file.pdf',
            PromptType.CONTEXT,
            'Prompt'
        ),
        (
            '/context:1?file="file.pdf" Prompt',
            '',
            1,
            'file.pdf',
            PromptType.CONTEXT,
            'Prompt'
        ),
        (
            '/context?file="my file-name_1.pdf" Prompt',
            '',
            DEFAULT_SIMILARITY_TOP_K,
            'my file-name_1.pdf',
            PromptType.CONTEXT,
            'Prompt'
        ),
        (
            '/context:1?file="my file-name_1.pdf" Prompt',
            '',
            1,
            'my file-name_1.pdf',
            PromptType.CONTEXT,
            'Prompt'
        ),
        (
            '/get:http://localhost',
            '',
            DEFAULT_SIMILARITY_TOP_K,
            '',
            PromptType.ENDPOINT,
            'http://localhost'
        ),
        (
            '/get:http://localhost:3000/data/1?query=value',
            '',
            DEFAULT_SIMILARITY_TOP_K,
            '',
            PromptType.ENDPOINT,
            'http://localhost:3000/data/1?query=value'
        ),
        (
            ':label Prompt',
            'label',
            DEFAULT_SIMILARITY_TOP_K,
            '',
            PromptType.GENERATE,
            'Prompt'
        ),
        (
            ':label Prompt one',
            'label',
            DEFAULT_SIMILARITY_TOP_K,
            '',
            PromptType.GENERATE,
            'Prompt one'
        ),
        (
            ':label Prompt one two',
            'label',
            DEFAULT_SIMILARITY_TOP_K,
            '',
            PromptType.GENERATE,
            'Prompt one two'
        ),
        (
            ':label Multline\nprompt',
            'label',
            DEFAULT_SIMILARITY_TOP_K,
            '',
            PromptType.GENERATE,
            'Multline\nprompt'
        ),
        (
            ':label /context Prompt',
            'label',
            DEFAULT_SIMILARITY_TOP_K,
            '',
            PromptType.CONTEXT,
            'Prompt'
        ),
        (
            ':label /context Prompt one',
            'label',
            DEFAULT_SIMILARITY_TOP_K,
            '',
            PromptType.CONTEXT,
            'Prompt one'
        ),
        (
            ':label /context Prompt one two',
            'label',
            DEFAULT_SIMILARITY_TOP_K,
            '',
            PromptType.CONTEXT,
            'Prompt one two'
        ),
        (
            ':label /context Multline\nprompt',
            'label',
            DEFAULT_SIMILARITY_TOP_K,
            '',
            PromptType.CONTEXT,
            'Multline\nprompt'
        ),
        (
            ':label /context:1 Prompt',
            'label',
            1,
            '',
            PromptType.CONTEXT,
            'Prompt'
        ),
        (
            ':label /context:11 Prompt one',
            'label',
            11,
            '',
            PromptType.CONTEXT,
            'Prompt one'
        ),
        (
            ':label /context:111 Prompt one two',
            'label',
            111,
            '',
            PromptType.CONTEXT,
            'Prompt one two'
        ),
        (
            ':label /context:1111 Multline\nprompt',
            'label',
            1111,
            '',
            PromptType.CONTEXT,
            'Multline\nprompt'
        ),
        (
            ':label-two Prompt',
            'label-two',
            DEFAULT_SIMILARITY_TOP_K,
            '',
            PromptType.GENERATE,
            'Prompt'
        ),
        (
            ':label-two Prompt one',
            'label-two',
            DEFAULT_SIMILARITY_TOP_K,
            '',
            PromptType.GENERATE,
            'Prompt one'
        ),
        (
            ':label-two Prompt one two',
            'label-two',
            DEFAULT_SIMILARITY_TOP_K,
            '',
            PromptType.GENERATE,
            'Prompt one two'
        ),
        (
            ':label-two Multline\nprompt',
            'label-two',
            DEFAULT_SIMILARITY_TOP_K,
            '',
            PromptType.GENERATE,
            'Multline\nprompt'
        ),
        (
            ':label-two /context Prompt',
            'label-two',
            DEFAULT_SIMILARITY_TOP_K,
            '',
            PromptType.CONTEXT,
            'Prompt'
        ),
        (
            ':label-two /context Prompt one',
            'label-two',
            DEFAULT_SIMILARITY_TOP_K,
            '',
            PromptType.CONTEXT,
            'Prompt one'
        ),
        (
            ':label-two /context Prompt one two',
            'label-two',
            DEFAULT_SIMILARITY_TOP_K,
            '',
            PromptType.CONTEXT,
            'Prompt one two'
        ),
        (
            ':label-two /context Multline\nprompt',
            'label-two',
            DEFAULT_SIMILARITY_TOP_K,
            '',
            PromptType.CONTEXT,
            'Multline\nprompt'
        ),
        (
            ':label-two /context:1 Prompt',
            'label-two',
            1,
            '',
            PromptType.CONTEXT,
            'Prompt'
        ),
        (
            ':label-two /context:11 Prompt one',
            'label-two',
            11,
            '',
            PromptType.CONTEXT,
            'Prompt one'
        ),
        (
            ':label-two /context:111 Prompt one two',
            'label-two',
            111,
            '',
            PromptType.CONTEXT,
            'Prompt one two'
        ),
        (
            ':label-two /context:1111 Multline\nprompt',
            'label-two',
            1111,
            '',
            PromptType.CONTEXT,
            'Multline\nprompt'
        ),
        (
            ':label /context?file="my file-name_1.pdf" Prompt',
            'label',
            DEFAULT_SIMILARITY_TOP_K,
            'my file-name_1.pdf',
            PromptType.CONTEXT,
            'Prompt'
        ),
        (
            ':label /context:1?file="my file-name_1.pdf" Prompt',
            'label',
            1,
            'my file-name_1.pdf',
            PromptType.CONTEXT,
            'Prompt'
        ),
        (
            ':label /get:http://localhost',
            'label',
            DEFAULT_SIMILARITY_TOP_K,
            '',
            PromptType.ENDPOINT,
            'http://localhost'
        ),
        (
            ':label /get:http://localhost:3000/data/1?query=value',
            'label',
            DEFAULT_SIMILARITY_TOP_K,
            '',
            PromptType.ENDPOINT,
            'http://localhost:3000/data/1?query=value'
        ),
        (
            '/echo Prompt',
            '',
            DEFAULT_SIMILARITY_TOP_K,
            '',
            PromptType.ECHO,
            'Prompt'
        ),
        (
            ':label /echo Prompt',
            'label',
            DEFAULT_SIMILARITY_TOP_K,
            '',
            PromptType.ECHO,
            'Prompt'
        )
    ]
)
def test_prompt_processing(
        prompt,
        label,
        top_k,
        file_name,
        prompt_type,
        actual_prompt):
    prompt_processor = Prompt(prompt)

    assert prompt_processor.get_original_prompt() == prompt
    assert prompt_processor.get_label() == label
    assert prompt_processor.get_top_k() == top_k
    assert prompt_processor.get_file_name() == file_name
    assert prompt_processor.get_prompt_type() == prompt_type
    assert prompt_processor.get_prompt() == actual_prompt
