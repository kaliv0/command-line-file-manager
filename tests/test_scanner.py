from app.utils import scanner


RESOURCE_DIR = "tests/resources"


def test_scan_files(runner):
    # case 0: test with default option values
    result = runner.invoke(scanner.scan_files, [RESOURCE_DIR])
    assert result.exit_code == 0
    assert result.output == (
        "The given directory 'tests/resources' contains the following files:\n"
        "\n"
        ".hidden_file.md\n"
        "audio1.wav\n"
        "file.txt\n"
        "file1.pdf\n"
        "pic.png\n"
        "pic1.jpg\n"
        "smth.md\n"
        "video.mp4\n"
        "\n"
        "=========================================\n"
        "\n"
    )


def test_scan_subdirs(runner):
    # case 0: test with default option values
    result = runner.invoke(scanner.scan_subdirs, [RESOURCE_DIR])
    assert result.exit_code == 0
    assert result.output == (
        "The given directory 'tests/resources' contains the following subdirectories:\n"
        "\n"
        ".hidden_other\n"
        "inner_test\n"
        "\n"
        "=========================================\n"
        "\n"
    )


def test_build_catalog(runner):
    # case 0: test with default option values
    result = runner.invoke(scanner.build_catalog, [RESOURCE_DIR])
    assert result.exit_code == 0
    assert result.output == (
        "The given directory 'tests/resources' contains the following files:\n"
        "\n"
        "pic1.jpg\n"
        "pic.png\n"
        ".hidden_file.md\n"
        "audio1.wav\n"
        "smth.md\n"
        "video.mp4\n"
        "file.txt\n"
        "file1.pdf\n"
        "\n"
        "=========================================\n"
        "The given directory 'tests/resources' contains the following subdirectories:\n"
        "\n"
        "inner_test\n"
        ".hidden_other\n"
        "\n"
        "=========================================\n"
        "\n"
    )
