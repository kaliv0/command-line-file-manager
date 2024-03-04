from app.cli import commands
from tests.conftest import RESOURCE_DIR


def test_scan_files(runner):
    # case 0: test with default option values
    result = runner.invoke(commands.scan_files, [RESOURCE_DIR])
    assert result.exit_code == 0
    message_substrings = (
        "The given directory 'tests/resources/plain' contains the following files:\n",
        ".hidden_file.md\n",
        "audio1.wav\n",
        "file.txt\n",
        "file1.pdf\n",
        "pic.png\n",
        "pic1.jpg\n",
        "smth.md\n",
        "video.mp4\n",
        "=========================================\n",
    )
    assert all(substring in result.output for substring in message_substrings)

    # case 1: test with sort option
    result = runner.invoke(commands.scan_files, [RESOURCE_DIR, "--sort=name", "--desc"])
    assert result.exit_code == 0
    assert result.output == (
        "The given directory 'tests/resources/plain' contains the following files:\n"
        "\n"
        "video.mp4\n"
        "smth.md\n"
        "pic1.jpg\n"
        "pic.png\n"
        "file1.pdf\n"
        "file.txt\n"
        "audio1.wav\n"
        ".hidden_file.md\n"
        "\n=========================================\n"
        "\n"
    )


def test_scan_subdirs(runner):
    # case 0: test with default option values
    result = runner.invoke(commands.scan_subdirs, [RESOURCE_DIR])
    assert result.exit_code == 0
    message_substrings = (
        "The given directory 'tests/resources/plain' contains the following subdirectories:\n",
        ".hidden_other\n",
        "inner_test\n",
        "=========================================\n",
    )
    assert all(substring in result.output for substring in message_substrings)

    # case 1: test with sort option
    result = runner.invoke(commands.scan_subdirs, [RESOURCE_DIR, "--sort=size", "--desc"])
    assert result.exit_code == 0
    assert result.output == (
        "The given directory 'tests/resources/plain' contains the following subdirectories:\n"
        "\n"
        ".hidden_other\n"
        "inner_test\n"
        "\n=========================================\n"
        "\n"
    )


def test_build_catalog(runner):
    result = runner.invoke(commands.build_catalog, [RESOURCE_DIR])
    assert result.exit_code == 0
    message_substrings = (
        "The given directory 'tests/resources/plain' contains the following files:\n",
        "pic1.jpg\n",
        "pic.png\n",
        ".hidden_file.md\n",
        "audio1.wav\n",
        "smth.md\n",
        "video.mp4\n",
        "file.txt\n",
        "file1.pdf\n",
        "=========================================\n",
        "The given directory 'tests/resources/plain' contains the following subdirectories:\n",
        "inner_test\n",
        ".hidden_other\n",
        "=========================================\n",
    )
    assert all(substring in result.output for substring in message_substrings)


def test_search_by_name(runner):
    keyword = "hidden"
    result = runner.invoke(commands.search_by_name, [RESOURCE_DIR, keyword])
    assert result.exit_code == 0
    assert result.output == (
        "Inside directory 'tests/resources/plain' the given keyword 'hidden' was found\n"
        "- in the following file names:\n"
        "\t- .hidden_file.md\n"
        "- in the following subdirectory names:\n"
        "\t- .hidden_other\n"
        "\n"
    )


def test_search_by_name_recursively(runner):
    keyword = "hidden"
    result = runner.invoke(commands.search_by_name_recursively, [RESOURCE_DIR, keyword])
    assert result.exit_code == 0
    message_substrings = [
        (
            "Inside directory 'tests/resources/plain' the given keyword 'hidden' was found\n"
            "- in the following file names:\n"
            "\t- .hidden_file.md\n"
            "- in the following subdirectory names:\n"
            "\t- .hidden_other\n"
            "\n=========================================\n"
        ),
        (
            "Inside directory 'tests/resources/plain/inner_test' the given keyword 'hidden' was found\n"
            "- in the following file names:\n\t- .inner_hidden_alone.wav\n- in the following subdirectory names:\n"
            "\t- .inner_hidden\n"
            "\n=========================================\n"
        ),
        (
            "Inside directory 'tests/resources/plain/inner_test/.inner_hidden' the given keyword 'hidden' was found\n"
            "- in the following file names:\n"
            "\t- .inner_hidden_music.mp3\n"
            "\n=========================================\n"
        ),
        (
            "Inside directory 'tests/resources/plain/.hidden_other' the given keyword 'hidden' was found\n"
            "- in the following file names:\n"
            "\t- .inside_hidden_other.md\n"
            "\n=========================================\n"
        ),
    ]
    assert all(substring in result.output for substring in message_substrings)
