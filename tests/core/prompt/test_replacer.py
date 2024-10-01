"""Tests for PromptPatternReplacer class."""

import pytest

from core.prompt import PromptHistory, PromptPatternReplacer


@pytest.fixture()
def replacer(history: PromptHistory) -> PromptPatternReplacer:
    return PromptPatternReplacer(history)


def test_replace_last_no_entries(replacer):
    prompt = """
Prompt to perform an action
-------------------
{response:last}
-------------------
Rest of the prompt
"""

    expected_replaced_prompt = """
Prompt to perform an action
-------------------

-------------------
Rest of the prompt
"""

    replaced_prompt = replacer.replace(prompt)

    assert replaced_prompt == expected_replaced_prompt


def test_replace_last_single_entry(replacer, history, entry1):
    history.append(entry1)

    prompt = """
Prompt to perform an action
-------------------
{response:last}
-------------------
Rest of the prompt
"""

    expected_replaced_prompt = f"""
Prompt to perform an action
-------------------
{entry1.response.value}
-------------------
Rest of the prompt
"""

    replaced_prompt = replacer.replace(prompt)

    assert replaced_prompt == expected_replaced_prompt


def test_replace_last_multiple_entries(replacer, history, entry1, entry2):
    history.extend([entry1, entry2])

    prompt = """
Prompt to perform an action
-------------------
{response:last}
-------------------
Rest of the prompt
"""

    expected_replaced_prompt = f"""
Prompt to perform an action
-------------------
{entry2.response.value}
-------------------
Rest of the prompt
"""

    replaced_prompt = replacer.replace(prompt)

    assert replaced_prompt == expected_replaced_prompt


def test_replace_label_no_entries(replacer):
    prompt = """
Prompt to perform an action
-------------------
{response:label:my-label}
-------------------
Rest of the prompt
"""

    expected_replaced_prompt = """
Prompt to perform an action
-------------------

-------------------
Rest of the prompt
"""

    replaced_prompt = replacer.replace(prompt)

    assert replaced_prompt == expected_replaced_prompt


def test_replace_label_single_entry(replacer, history, entry1):
    history.append(entry1)

    prompt = f"""
Prompt to perform an action
-------------------
{{response:label:{entry1.label}}}
-------------------
Rest of the prompt
"""

    expected_replaced_prompt = f"""
Prompt to perform an action
-------------------
{entry1.response.value}
-------------------
Rest of the prompt
"""

    replaced_prompt = replacer.replace(prompt)

    assert replaced_prompt == expected_replaced_prompt


def test_replace_label_multiple_entries(replacer, history, entry1, entry2):
    history.extend([entry1, entry2])

    prompt = f"""
Prompt to perform an action
-------------------
{{response:label:{entry1.label}}}
---
{{response:label:{entry2.label}}}
{{response:last}}
-------------------
Rest of the prompt
"""

    expected_replaced_prompt = f"""
Prompt to perform an action
-------------------
{entry1.response.value}
---
{entry2.response.value}
{entry2.response.value}
-------------------
Rest of the prompt
"""

    replaced_prompt = replacer.replace(prompt)

    assert replaced_prompt == expected_replaced_prompt
