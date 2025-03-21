from tests.conftest import compare

RESOURCE_DIR = "tests/resources/plain"


def test_scan_files(runner):
    result = runner.invoke(commands.scan_files, [RESOURCE_DIR])
    assert result.exit_code == 0
    message_substrings = (
        "'tests/resources/plain' contains the following files:\n",
        "\t- .hidden_file.md\n",
        "\t- audio1.wav\n",
        "\t- file.txt\n",
        "\t- file1.pdf\n",
        "\t- pic.png\n",
        "\t- pic1.jpg\n",
        "\t- smth.md\n",
        "\t- video.mp4\n",
        "=========================================\n",
    )
    assert all(substring in result.output for substring in message_substrings)


def test_scan_files_sorted(runner):
    result = runner.invoke(commands.scan_files, [RESOURCE_DIR, "--sort=name", "--desc"])
    assert result.exit_code == 0
    assert result.output == (
        "'tests/resources/plain' contains the following files:\n"
        "\t- video.mp4\n"
        "\t- smth.md\n"
        "\t- pic1.jpg\n"
        "\t- pic.png\n"
        "\t- file1.pdf\n"
        "\t- file.txt\n"
        "\t- audio1.wav\n"
        "\t- .hidden_file.md\n"
        "=========================================\n\n"
    )


def test_scan_subdirs(runner):
    result = runner.invoke(commands.scan_subdirs, [RESOURCE_DIR])
    assert result.exit_code == 0
    message_substrings = (
        "'tests/resources/plain' contains the following subdirectories:\n",
        "\t- .hidden_other\n",
        "\t- inner_test\n",
        "=========================================\n",
    )
    assert all(substring in result.output for substring in message_substrings)


def test_scan_subdirs_sorted(runner):
    result = runner.invoke(commands.scan_subdirs, [RESOURCE_DIR, "--sort=size", "--desc"])
    assert result.exit_code == 0
    assert result.output == (
        "'tests/resources/plain' contains the following subdirectories:\n"
        "\t- .hidden_other\n"
        "\t- inner_test\n"
        "=========================================\n\n"
    )


def test_build_catalog(runner):
    result = runner.invoke(commands.build_catalog, [RESOURCE_DIR])
    assert result.exit_code == 0
    message_substrings = (
        "'tests/resources/plain' contains the following files:\n",
        "\t- pic1.jpg\n",
        "\t- pic.png\n",
        "\t- .hidden_file.md\n",
        "\t- audio1.wav\n",
        "\t- smth.md\n",
        "\t- video.mp4\n",
        "\t- file.txt\n",
        "\t- file1.pdf\n",
        "=========================================\n",
        "'tests/resources/plain' contains the following subdirectories:\n",
        "\t- inner_test\n",
        "\t- .hidden_other\n",
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
            "=========================================\n"
        ),
        (
            "Inside directory 'tests/resources/plain/inner_test' the given keyword 'hidden' was found\n"
            "- in the following file names:\n\t- .inner_hidden_alone.wav\n- in the following subdirectory names:\n"
            "\t- .inner_hidden\n"
            "=========================================\n"
        ),
        (
            "Inside directory 'tests/resources/plain/inner_test/.inner_hidden' the given keyword 'hidden' was found\n"
            "- in the following file names:\n"
            "\t- .inner_hidden_music.mp3\n"
            "=========================================\n"
        ),
        (
            "Inside directory 'tests/resources/plain/.hidden_other' the given keyword 'hidden' was found\n"
            "- in the following file names:\n"
            "\t- .inside_hidden_other.md\n"
            "=========================================\n"
        ),
    ]
    assert all(substring in result.output for substring in message_substrings)


def test_compare_dirs(runner, tmp_cmp_dirs):
    source, target = tmp_cmp_dirs
    result = runner.invoke(commands.compare_directories, [source, target])
    assert result.exit_code == 0
    assert compare(source, target) == (2, 3, 1)
