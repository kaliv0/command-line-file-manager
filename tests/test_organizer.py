import os
from manager.cli import commands

DUPLICATES_RESOURCE_DIR = "tests/resources/duplicates"


def test_handle_duplicate_files(runner, mock_organizer):
    result = runner.invoke(commands.handle_duplicate_files, [DUPLICATES_RESOURCE_DIR])
    assert result.exit_code == 0

    log_message = _cleanup_abs_paths(result, DUPLICATES_RESOURCE_DIR)
    message_substrings = (
        "Skipping .hidden1.txt\n",
        "Skipping .hidden2.txt\n",
        "'tests/resources/duplicates' contains the following duplicate files:\n\n",
        "log1.md\n",
        "log2.md\n",
        "-----------------------------------------\n",
        "book1.txt\n",
        "book2.txt\n",
        "-----------------------------------------\n\n",
        "Merging duplicates: ['log1.md', 'log2.md'] into log1.md\n",
        "Merging duplicates: ['book1.txt', 'book2.txt'] into book1.txt\n",
    )
    assert all(substring in log_message for substring in message_substrings)


def test_handle_duplicate_files_hidden(runner, mock_organizer):
    result = runner.invoke(commands.handle_duplicate_files, ["-h", DUPLICATES_RESOURCE_DIR])
    assert result.exit_code == 0

    log_message = _cleanup_abs_paths(result, DUPLICATES_RESOURCE_DIR)
    message_substrings = (
        "'tests/resources/duplicates' contains the following duplicate files:\n\n",
        "log1.md\n",
        "log2.md\n",
        "-----------------------------------------\n",
        "book1.txt\n",
        "book2.txt\n",
        "-----------------------------------------\n\n",
        "Merging duplicates: ['log1.md', 'log2.md'] into log1.md\n",
        "Merging duplicates: ['book1.txt', 'book2.txt'] into book1.txt\n",
    )
    assert all(substring in log_message for substring in message_substrings)


def test_handle_duplicate_files_recursively(runner, mock_organizer):
    result = runner.invoke(commands.handle_duplicate_files, [DUPLICATES_RESOURCE_DIR])
    assert result.exit_code == 0

    log_message = _cleanup_abs_paths(result, DUPLICATES_RESOURCE_DIR)
    message_substrings = (
        "Skipping .hidden1.txt\n",
        "Skipping .hidden2.txt\n",
        "'tests/resources/duplicates' contains the following duplicate files:\n\n",
        "log1.md\n",
        "log2.md\n",
        "-----------------------------------------\n",
        "book1.txt\n",
        "book2.txt\n",
        "-----------------------------------------\n\n",
        "Merging duplicates: ['log1.md', 'log2.md'] into log1.md\n",
        "Merging duplicates: ['book1.txt', 'book2.txt'] into book1.txt\n",
    )
    assert all(substring in log_message for substring in message_substrings)


def test_handle_duplicate_files_recursively_hidden(runner, mock_organizer):
    result = runner.invoke(commands.handle_duplicate_files, ["-h", DUPLICATES_RESOURCE_DIR])
    assert result.exit_code == 0

    log_message = _cleanup_abs_paths(result, DUPLICATES_RESOURCE_DIR)
    message_substrings = (
        "'tests/resources/duplicates' contains the following duplicate files:\n\n",
        ".hidden1.txt\n",
        ".hidden2.txt\n",
        "-----------------------------------------\n",
        "log1.md\n",
        "log2.md\n",
        "book1.txt\n",
        "book2.txt\n",
        "-----------------------------------------\n\n",
        "Merging duplicates: ['.hidden1.txt', '.hidden2.txt'] into .hidden1.txt\n",
        "Merging duplicates: ['log1.md', 'log2.md'] into log1.md\n",
        "Merging duplicates: ['book1.txt', 'book2.txt'] into book1.txt\n",
    )
    assert all(substring in log_message for substring in message_substrings)


def _cleanup_abs_paths(result, resource_dir):
    resources_full_path = os.path.abspath(resource_dir)
    return result.output.replace(resources_full_path, resource_dir)
