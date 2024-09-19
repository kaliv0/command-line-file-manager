import os

from app.cli import commands
from tests.conftest import DUPLICATES_RESOURCE_DIR, RESOURCE_DIR


def test_organize_files(runner, mock_organizer):
    result = runner.invoke(commands.organize_files, [RESOURCE_DIR])
    assert result.exit_code == 0

    log_message = _cleanup_abs_paths(result)
    message_substrings = (
        "Creating folder tests/resources/plain/images\n",
        "Moving pic1.jpg to tests/resources/plain/images\n",
        "Creating folder tests/resources/plain/images\n",
        "Moving pic.png to tests/resources/plain/images\n",
        "Skipping .hidden_file.md\n",
        "Creating folder tests/resources/plain/music\n",
        "Moving audio1.wav to tests/resources/plain/music\n",
        "Creating folder tests/resources/plain/other\n",
        "Moving smth.md to tests/resources/plain/other\n",
        "Creating folder tests/resources/plain/videos\n",
        "Moving video.mp4 to tests/resources/plain/videos\n",
        "Creating folder tests/resources/plain/docs\n",
        "Moving file.txt to tests/resources/plain/docs\n",
        "Creating folder tests/resources/plain/books\n",
        "Moving file1.pdf to tests/resources/plain/books\n",
    )
    assert all(substring in log_message for substring in message_substrings)


def test_handle_duplicate_files(runner, mock_organizer):
    result = runner.invoke(commands.handle_duplicate_files, [DUPLICATES_RESOURCE_DIR])
    assert result.exit_code == 0

    resources_full_path = os.path.abspath(DUPLICATES_RESOURCE_DIR)
    log_message = result.output.replace(resources_full_path, DUPLICATES_RESOURCE_DIR)
    message_substrings = (
        "Skipping .hidden1.txt\n",
        "Skipping .hidden2.txt\n",
        "The given directory 'tests/resources/duplicates' contains the following duplicate files:\n\n",
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

    resources_full_path = os.path.abspath(DUPLICATES_RESOURCE_DIR)
    log_message = result.output.replace(resources_full_path, DUPLICATES_RESOURCE_DIR)
    message_substrings = (
        "The given directory 'tests/resources/duplicates' contains the following duplicate files:\n\n",
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

    resources_full_path = os.path.abspath(DUPLICATES_RESOURCE_DIR)
    log_message = result.output.replace(resources_full_path, DUPLICATES_RESOURCE_DIR)
    message_substrings = (
        "Skipping .hidden1.txt\n",
        "Skipping .hidden2.txt\n",
        "The given directory 'tests/resources/duplicates' contains the following duplicate files:\n\n",
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

    resources_full_path = os.path.abspath(DUPLICATES_RESOURCE_DIR)
    log_message = result.output.replace(resources_full_path, DUPLICATES_RESOURCE_DIR)
    message_substrings = (
        "The given directory 'tests/resources/duplicates' contains the following duplicate files:\n\n",
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


def _cleanup_abs_paths(result):
    resources_full_path = os.path.abspath(RESOURCE_DIR)
    log_message = result.output.replace(resources_full_path, RESOURCE_DIR)
    return log_message
