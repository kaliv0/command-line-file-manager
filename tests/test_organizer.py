import os

from manager.cli import commands
from tests.util import compare

RESOURCE_DIR = "tests/resources/plain"
DUPLICATES_RESOURCE_DIR = "tests/resources/duplicates"


def test_organize_files(runner, tmp_dirs):
    source, target = tmp_dirs
    result = runner.invoke(commands.organize_files, ["-h", source])
    assert result.exit_code == 0
    assert compare(source, target) == (0, 0, 0)


def test_handle_duplicate_files(runner, mock_organizer):
    result = runner.invoke(commands.handle_duplicate_files, [DUPLICATES_RESOURCE_DIR])
    assert result.exit_code == 0

    log_message = _cleanup_abs_paths(result, DUPLICATES_RESOURCE_DIR)
    message_substrings = (
        "Skipping .hidden1.txt\n",
        "Skipping .hidden2.txt\n",
        "'tests/resources/duplicates' contains the following duplicate files:\n",
        "\t- log1.md\n",
        "\t- log2.md\n",
        "-----------------------------------------\n",
        "\t- book1.txt\n",
        "\t- book2.txt\n",
        "-----------------------------------------\n",
        "Merging duplicates: ['log1.md', 'log2.md'] into log1.md\n",
        "Merging duplicates: ['book1.txt', 'book2.txt'] into book1.txt\n",
    )
    assert all(substring in log_message for substring in message_substrings)


def test_handle_duplicate_files_hidden(runner, mock_organizer):
    result = runner.invoke(commands.handle_duplicate_files, ["-h", DUPLICATES_RESOURCE_DIR])
    assert result.exit_code == 0

    log_message = _cleanup_abs_paths(result, DUPLICATES_RESOURCE_DIR)
    message_substrings = (
        "'tests/resources/duplicates' contains the following duplicate files:\n",
        "\t- log1.md\n",
        "\t- log2.md\n",
        "-----------------------------------------\n",
        "\t- book1.txt\n",
        "\t- book2.txt\n",
        "-----------------------------------------\n",
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
        "'tests/resources/duplicates' contains the following duplicate files:\n",
        "\t- log1.md\n",
        "\t- log2.md\n",
        "-----------------------------------------\n",
        "\t- book1.txt\n",
        "\t- book2.txt\n",
        "-----------------------------------------\n",
        "Merging duplicates: ['log1.md', 'log2.md'] into log1.md\n",
        "Merging duplicates: ['book1.txt', 'book2.txt'] into book1.txt\n",
    )
    assert all(substring in log_message for substring in message_substrings)


def test_handle_duplicate_files_recursively_hidden(runner, mock_organizer):
    result = runner.invoke(commands.handle_duplicate_files, ["-h", DUPLICATES_RESOURCE_DIR])
    assert result.exit_code == 0

    log_message = _cleanup_abs_paths(result, DUPLICATES_RESOURCE_DIR)
    message_substrings = (
        "'tests/resources/duplicates' contains the following duplicate files:\n",
        "\t- .hidden1.txt\n",
        "\t- .hidden2.txt\n",
        "-----------------------------------------\n",
        "\t- log1.md\n",
        "\t- log2.md\n",
        "\t- book1.txt\n",
        "\t- book2.txt\n",
        "-----------------------------------------\n",
        "Merging duplicates: ['.hidden1.txt', '.hidden2.txt'] into .hidden1.txt\n",
        "Merging duplicates: ['log1.md', 'log2.md'] into log1.md\n",
        "Merging duplicates: ['book1.txt', 'book2.txt'] into book1.txt\n",
    )
    assert all(substring in log_message for substring in message_substrings)


def _cleanup_abs_paths(result, resource_dir):
    resources_full_path = os.path.abspath(resource_dir)
    return result.output.replace(resources_full_path, resource_dir)
