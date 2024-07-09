"""Tests for Operator objects."""

import pytest

from llm.operator import DEFAULT_SIMILARITY_TOP_K, PromptProcessor


class TestPromptProcessor():
    @pytest.mark.parametrize(
        'prompt,label,top_k,is_context_prompt,actual_prompt', [
            (
                'Prompt',
                '',
                DEFAULT_SIMILARITY_TOP_K,
                False,
                'Prompt'
            ),
            (
                'Prompt one',
                '',
                DEFAULT_SIMILARITY_TOP_K,
                False,
                'Prompt one'
            ),
            (
                'Prompt one two',
                '',
                DEFAULT_SIMILARITY_TOP_K,
                False,
                'Prompt one two'
            ),
            (
                'Multline\nprompt',
                '',
                DEFAULT_SIMILARITY_TOP_K,
                False,
                'Multline\nprompt'
            ),
            (
                '/context Prompt',
                '',
                DEFAULT_SIMILARITY_TOP_K,
                True,
                'Prompt'
            ),
            (
                '/context Prompt one',
                '',
                DEFAULT_SIMILARITY_TOP_K,
                True,
                'Prompt one'
            ),
            (
                '/context Prompt one two',
                '',
                DEFAULT_SIMILARITY_TOP_K,
                True,
                'Prompt one two'
            ),
            (
                '/context Multline\nprompt',
                '',
                DEFAULT_SIMILARITY_TOP_K,
                True,
                'Multline\nprompt'
            ),
            (
                '/context:1 Prompt',
                '',
                1,
                True,
                'Prompt'
            ),
            (
                '/context:11 Prompt one',
                '',
                11,
                True,
                'Prompt one'
            ),
            (
                '/context:111 Prompt one two',
                '',
                111,
                True,
                'Prompt one two'
            ),
            (
                '/context:1111 Multline\nprompt',
                '',
                1111,
                True,
                'Multline\nprompt'
            ),
            (
                ':label Prompt',
                'label',
                DEFAULT_SIMILARITY_TOP_K,
                False,
                'Prompt'
            ),
            (
                ':label Prompt one',
                'label',
                DEFAULT_SIMILARITY_TOP_K,
                False,
                'Prompt one'
            ),
            (
                ':label Prompt one two',
                'label',
                DEFAULT_SIMILARITY_TOP_K,
                False,
                'Prompt one two'
            ),
            (
                ':label Multline\nprompt',
                'label',
                DEFAULT_SIMILARITY_TOP_K,
                False,
                'Multline\nprompt'
            ),
            (
                ':label /context Prompt',
                'label',
                DEFAULT_SIMILARITY_TOP_K,
                True,
                'Prompt'
            ),
            (
                ':label /context Prompt one',
                'label',
                DEFAULT_SIMILARITY_TOP_K,
                True,
                'Prompt one'
            ),
            (
                ':label /context Prompt one two',
                'label',
                DEFAULT_SIMILARITY_TOP_K,
                True,
                'Prompt one two'
            ),
            (
                ':label /context Multline\nprompt',
                'label',
                DEFAULT_SIMILARITY_TOP_K,
                True,
                'Multline\nprompt'
            ),
            (
                ':label /context:1 Prompt',
                'label',
                1,
                True,
                'Prompt'
            ),
            (
                ':label /context:11 Prompt one',
                'label',
                11,
                True,
                'Prompt one'
            ),
            (
                ':label /context:111 Prompt one two',
                'label',
                111,
                True,
                'Prompt one two'
            ),
            (
                ':label /context:1111 Multline\nprompt',
                'label',
                1111,
                True,
                'Multline\nprompt'
            ),
            (
                ':label-two Prompt',
                'label-two',
                DEFAULT_SIMILARITY_TOP_K,
                False,
                'Prompt'
            ),
            (
                ':label-two Prompt one',
                'label-two',
                DEFAULT_SIMILARITY_TOP_K,
                False,
                'Prompt one'
            ),
            (
                ':label-two Prompt one two',
                'label-two',
                DEFAULT_SIMILARITY_TOP_K,
                False,
                'Prompt one two'
            ),
            (
                ':label-two Multline\nprompt',
                'label-two',
                DEFAULT_SIMILARITY_TOP_K,
                False,
                'Multline\nprompt'
            ),
            (
                ':label-two /context Prompt',
                'label-two',
                DEFAULT_SIMILARITY_TOP_K,
                True,
                'Prompt'
            ),
            (
                ':label-two /context Prompt one',
                'label-two',
                DEFAULT_SIMILARITY_TOP_K,
                True,
                'Prompt one'
            ),
            (
                ':label-two /context Prompt one two',
                'label-two',
                DEFAULT_SIMILARITY_TOP_K,
                True,
                'Prompt one two'
            ),
            (
                ':label-two /context Multline\nprompt',
                'label-two',
                DEFAULT_SIMILARITY_TOP_K,
                True,
                'Multline\nprompt'
            ),
            (
                ':label-two /context:1 Prompt',
                'label-two',
                1,
                True,
                'Prompt'
            ),
            (
                ':label-two /context:11 Prompt one',
                'label-two',
                11,
                True,
                'Prompt one'
            ),
            (
                ':label-two /context:111 Prompt one two',
                'label-two',
                111,
                True,
                'Prompt one two'
            ),
            (
                ':label-two /context:1111 Multline\nprompt',
                'label-two',
                1111,
                True,
                'Multline\nprompt'
            )
        ]
    )
    def test_prompt_processing(
            self,
            prompt,
            label,
            top_k,
            is_context_prompt,
            actual_prompt):
        prompt_processor = PromptProcessor(prompt)

        assert prompt_processor.get_label() == label
        assert prompt_processor.get_top_k() == top_k
        assert prompt_processor.is_context_prompt() == is_context_prompt
        assert prompt_processor.get_prompt() == actual_prompt
