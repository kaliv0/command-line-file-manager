from app.utils import scanner
from tests.conftest import RESOURCE_DIR


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

    # case 1: test with sort option
    result = runner.invoke(scanner.scan_files, [RESOURCE_DIR, "--sort=Name", "--desc"])
    assert result.exit_code == 0
    assert result.output == (
        "The given directory 'tests/resources' contains the following files:\n"
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

    # case 1: test with sort option
    result = runner.invoke(scanner.scan_subdirs, [RESOURCE_DIR, "--sort=date", "--desc"])
    assert result.exit_code == 0
    assert result.output == (
        "The given directory 'tests/resources' contains the following subdirectories:\n"
        "\n"
        "inner_test\n"
        ".hidden_other\n"
        "\n=========================================\n"
        "\n"
    )


def test_build_catalog(runner):
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


def test_build_catalog_recursively(runner):
    result = runner.invoke(scanner.build_catalog_recursively, [RESOURCE_DIR])
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
        "The given directory 'tests/resources' contains the following "
        "subdirectories:\n"
        "\n"
        "inner_test\n"
        ".hidden_other\n"
        "\n"
        "=========================================\n"
        "The given directory 'tests/resources/inner_test' contains the following "
        "files:\n"
        "\n"
        "inner_file1.pdf\n"
        "inner_pic.png\n"
        "inner_file.txt\n"
        "inner_smth.md\n"
        ".inner_hidden_alone.wav\n"
        "inner_audio1.wav\n"
        "inner_audio.mp4\n"
        "inner_pic1.jpg\n"
        "\n"
        "=========================================\n"
        "The given directory 'tests/resources/inner_test' contains the following "
        "subdirectories:\n"
        "\n"
        "most_inner_test\n"
        ".inner_hidden\n"
        "\n"
        "=========================================\n"
        "The given directory 'tests/resources/inner_test/most_inner_test' contains "
        "the following files:\n"
        "\n"
        "most_inner_file1.pdf\n"
        "most_inner_file.txt\n"
        "most_inner_pic1.jpg\n"
        "most_inner_audio.mp4\n"
        "most_inner_audio1.wav\n"
        "most_inner_pic.png\n"
        "most_inner_smth.md\n"
        "\n"
        "=========================================\n"
        "The given directory 'tests/resources/inner_test/most_inner_test' contains "
        "the following subdirectories:\n"
        "\n"
        "music\n"
        "\n"
        "=========================================\n"
        "The given directory 'tests/resources/inner_test/most_inner_test/music' "
        "contains the following files:\n"
        "\n"
        "inside_most_inner_audio.wav\n"
        "\n"
        "=========================================\n"
        "The given directory 'tests/resources/inner_test/most_inner_test/music' "
        "contains no nested subdirectories:\n"
        "\n"
        "\n"
        "=========================================\n"
        "The given directory 'tests/resources/inner_test/.inner_hidden' contains the "
        "following files:\n"
        "\n"
        ".inner_hidden_music.mp3\n"
        "\n"
        "=========================================\n"
        "The given directory 'tests/resources/inner_test/.inner_hidden' contains no "
        "nested subdirectories:\n"
        "\n"
        "\n"
        "=========================================\n"
        "The given directory 'tests/resources/.hidden_other' contains the following "
        "files:\n"
        "\n"
        ".inside_hidden_other.md\n"
        "\n"
        "=========================================\n"
        "The given directory 'tests/resources/.hidden_other' contains no nested "
        "subdirectories:\n"
        "\n"
        "\n"
        "=========================================\n"
        "\n"
    )


def test_build_tree(runner):
    result = runner.invoke(scanner.build_tree, [RESOURCE_DIR])
    assert result.exit_code == 0
    assert result.output == (
        "📁 /home/kaliv0/PycharmProjects/Advanced_File_Manager/tests/resources/\n"
        "    📃 pic1.jpg\n"
        "    📃 pic.png\n"
        "    📃 .hidden_file.md\n"
        "    📃 audio1.wav\n"
        "    📃 smth.md\n"
        "    📃 video.mp4\n"
        "    📃 file.txt\n"
        "    📃 file1.pdf\n"
        "    📁 "
        "/home/kaliv0/PycharmProjects/Advanced_File_Manager/tests/resources/inner_test/\n"
        "        📃 inner_file1.pdf\n"
        "        📃 inner_pic.png\n"
        "        📃 inner_file.txt\n"
        "        📃 inner_smth.md\n"
        "        📃 .inner_hidden_alone.wav\n"
        "        📃 inner_audio1.wav\n"
        "        📃 inner_audio.mp4\n"
        "        📃 inner_pic1.jpg\n"
        "        📁 "
        "/home/kaliv0/PycharmProjects/Advanced_File_Manager/tests/resources/inner_test/most_inner_test/\n"
        "            📃 most_inner_file1.pdf\n"
        "            📃 most_inner_file.txt\n"
        "            📃 most_inner_pic1.jpg\n"
        "            📃 most_inner_audio.mp4\n"
        "            📃 most_inner_audio1.wav\n"
        "            📃 most_inner_pic.png\n"
        "            📃 most_inner_smth.md\n"
        "            📁 "
        "/home/kaliv0/PycharmProjects/Advanced_File_Manager/tests/resources/inner_test/most_inner_test/music/\n"
        "                📃 inside_most_inner_audio.wav\n"
        "        📁 "
        "/home/kaliv0/PycharmProjects/Advanced_File_Manager/tests/resources/inner_test/.inner_hidden/\n"
        "            📃 .inner_hidden_music.mp3\n"
        "    📁 "
        "/home/kaliv0/PycharmProjects/Advanced_File_Manager/tests/resources/.hidden_other/\n"
        "        📃 .inside_hidden_other.md\n"
        "\n"
    )


def test_build_pretty_tree(runner):
    result = runner.invoke(scanner.build_pretty_tree, [RESOURCE_DIR])
    assert result.exit_code == 0
    assert result.output == (
        "resources/\n"
        "├── audio1.wav\n"
        "├── file.txt\n"
        "├── file1.pdf\n"
        "├── inner_test/\n"
        "│   ├── inner_audio.mp4\n"
        "│   ├── inner_audio1.wav\n"
        "│   ├── inner_file.txt\n"
        "│   ├── inner_file1.pdf\n"
        "│   ├── inner_pic.png\n"
        "│   ├── inner_pic1.jpg\n"
        "│   ├── inner_smth.md\n"
        "│   └── most_inner_test/\n"
        "│       ├── most_inner_audio.mp4\n"
        "│       ├── most_inner_audio1.wav\n"
        "│       ├── most_inner_file.txt\n"
        "│       ├── most_inner_file1.pdf\n"
        "│       ├── most_inner_pic.png\n"
        "│       ├── most_inner_pic1.jpg\n"
        "│       ├── most_inner_smth.md\n"
        "│       └── music/\n"
        "│           └── inside_most_inner_audio.wav\n"
        "├── pic.png\n"
        "├── pic1.jpg\n"
        "├── smth.md\n"
        "└── video.mp4\n"
        "\n"
    )


def test_search_by_name(runner):
    keyword = "hidden"
    result = runner.invoke(scanner.search_by_name, [RESOURCE_DIR, keyword])
    assert result.exit_code == 0
    assert result.output == (
        "Inside directory 'tests/resources' the given keyword 'hidden' was found\n"
        "- in the following file names:\n"
        "\t- .hidden_file.md\n"
        "- in the following subdirectory names:\n"
        "\t- .hidden_other\n"
        "\n"
    )


def test_search_by_name_recursively(runner):
    keyword = "hidden"
    result = runner.invoke(scanner.search_by_name_recursively, [RESOURCE_DIR, keyword])
    assert result.exit_code == 0
    assert result.output == (
        "Inside directory 'tests/resources' the given keyword 'hidden' was found\n"
        "- in the following file names:\n"
        "\t- .hidden_file.md\n"
        "- in the following subdirectory names:\n"
        "\t- .hidden_other\n"
        "\n=========================================\n"
        "Inside directory 'tests/resources/inner_test' the given keyword 'hidden' was found\n"
        "- in the following file names:\n\t- .inner_hidden_alone.wav\n- in the following subdirectory names:\n"
        "\t- .inner_hidden\n"
        "\n=========================================\n"
        "Inside directory 'tests/resources/inner_test/.inner_hidden' the given keyword 'hidden' was found\n"
        "- in the following file names:\n"
        "\t- .inner_hidden_music.mp3\n"
        "\n=========================================\n"
        "Inside directory 'tests/resources/.hidden_other' the given keyword 'hidden' was found\n"
        "- in the following file names:\n"
        "\t- .inside_hidden_other.md\n"
        "\n=========================================\n"
        "\n"
    )
