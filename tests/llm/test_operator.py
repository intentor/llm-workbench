"""Tests for Operator objects."""

import pytest

from llm.operator import DEFAULT_SIMILARITY_TOP_K, PromptProcessor


class TestPromptProcessor():
    @pytest.mark.parametrize(
        'prompt,top_k,is_context_prompt,actual_prompt', [
            (
                '/context Context query',
                DEFAULT_SIMILARITY_TOP_K,
                True,
                'Context query'
            ),
            (
                '/context:1 Context query',
                1,
                True,
                'Context query'
            ),
            (
                '/context:11 Context query',
                11,
                True,
                'Context query'
            ),
            (
                '/context:111 Context query',
                111,
                True,
                'Context query'
            ),
            (
                'Prompt',
                DEFAULT_SIMILARITY_TOP_K,
                False,
                'Prompt'
            ),
            (
                'Multi-word prompt',
                DEFAULT_SIMILARITY_TOP_K,
                False,
                'Multi-word prompt',
            ),
            (
                'Multi-line\nprompt',
                DEFAULT_SIMILARITY_TOP_K,
                False,
                'Multi-line\nprompt',
            )
        ]
    )
    def test_prompt_processing(
            self,
            prompt,
            top_k,
            is_context_prompt,
            actual_prompt):
        prompt_processor = PromptProcessor(prompt)

        assert prompt_processor.get_top_k() == top_k
        assert prompt_processor.is_context_prompt() == is_context_prompt
        assert prompt_processor.get_prompt() == actual_prompt
