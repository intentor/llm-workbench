"""Tests for replace_previous_response functiom."""

from core.prompt import replace_response


def test_replace_last_no_entries(history):
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

    replaced_prompt = replace_response(prompt, history)

    assert replaced_prompt == expected_replaced_prompt


def test_replace_last_single_entry(history, entry1):
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
{entry1.response}
-------------------
Rest of the prompt
"""

    replaced_prompt = replace_response(prompt, history)

    assert replaced_prompt == expected_replaced_prompt


def test_replace_last_multiple_entries(history, entry1, entry2):
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
{entry2.response}
-------------------
Rest of the prompt
"""

    replaced_prompt = replace_response(prompt, history)

    assert replaced_prompt == expected_replaced_prompt
