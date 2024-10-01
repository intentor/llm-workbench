"""Fixtures for in the current namespace."""

from urllib import response
import pytest

from core.prompt import GeneratedResponse, PromptHistory, PromptHistoryEntry

TEST_LABEL1 = 'my-label1'
TEST_LABEL2 = 'my-label2'
TEST_PROMPT = 'Prompt'
TEST_RESPONSE = 'Response'


@pytest.fixture
def history() -> PromptHistory:
    return PromptHistory()


@pytest.fixture
def entry1() -> PromptHistoryEntry:
    return PromptHistoryEntry(
        label=TEST_LABEL1,
        prompt=TEST_PROMPT + TEST_LABEL1,
        response=GeneratedResponse(
            value=TEST_RESPONSE + TEST_LABEL1,
            input_tokens=5,
            output_tokens=10
        )
    )


@pytest.fixture
def entry2() -> PromptHistoryEntry:
    return PromptHistoryEntry(
        label=TEST_LABEL2,
        prompt=TEST_PROMPT + TEST_LABEL2,
        response=GeneratedResponse(
            value=TEST_RESPONSE + TEST_LABEL2,
            input_tokens=4,
            output_tokens=8
        )
    )
