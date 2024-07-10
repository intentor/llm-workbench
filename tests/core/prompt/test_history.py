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

    assert last_response == entry2.response


def test_get_response_by_label_single_entry(history, entry1, entry2):
    history.extend([entry1, entry2])

    entries = history.get_response_by_label(entry2.label)
    assert len(entries) == 1
    assert entries[0] == entry2.response


def test_get_response_by_label_multiple_entries(history, entry1, entry2):
    history.extend([entry1, entry1, entry2, entry2, entry2])

    entries = history.get_response_by_label(entry2.label)
    assert len(entries) == 3
    assert entries[0] == entry2.response
    assert entries[1] == entry2.response
    assert entries[2] == entry2.response
