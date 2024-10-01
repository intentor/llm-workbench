"""Tests for PromptHistory class."""


def test_add_entry(history, entry1):
    history.append(entry1)

    assert len(history) == 1


def test_get_prompts(history, entry1, entry2):
    history.extend([entry1, entry2])

    prompts = history.get_prompts()

    assert len(prompts) == 2
    assert prompts[0] == entry1.prompt
    assert prompts[1] == entry2.prompt


def test_get_last_response_no_entries(history):
    last_response = history.get_last_response()

    assert last_response == ''


def test_get_last_response_has_entries(history, entry1, entry2):
    history.extend([entry1, entry2])

    last_response = history.get_last_response()

    assert last_response == entry2.response.value


def test_get_response_by_label_single_entry(history, entry1, entry2):
    history.extend([entry1, entry2])

    entries = history.get_response_by_label(entry2.label)
    assert len(entries) == 1
    assert entries[0] == entry2.response.value


def test_get_response_by_label_multiple_entries(history, entry1, entry2):
    history.extend([entry1, entry1, entry2, entry2, entry2])

    entries = history.get_response_by_label(entry2.label)
    assert len(entries) == 3
    assert entries[0] == entry2.response.value
    assert entries[1] == entry2.response.value
    assert entries[2] == entry2.response.value


def test_get_history_as_string(history, entry1, entry2):
    history.extend([entry1, entry2])

    history_as_string = history.get_as_string()

    assert history_as_string == f"""{entry1.prompt}

{entry1.response.value}

{entry2.prompt}

{entry2.response.value}"""


def test_get_total_input_tokens(history, entry1, entry2):
    history.extend([entry1, entry2])

    expected_tokens = entry1.response.input_tokens + entry2.response.input_tokens
    calculated_tokens = history.get_total_input_tokens()

    assert calculated_tokens == expected_tokens


def test_get_total_output_tokens(history, entry1, entry2):
    history.extend([entry1, entry2])

    expected_tokens = entry1.response.output_tokens + entry2.response.output_tokens
    calculated_tokens = history.get_total_output_tokens()

    assert calculated_tokens == expected_tokens
