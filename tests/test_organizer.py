import os

from app.utils import organizer
from tests.conftest import RESOURCE_DIR


def test_organize_files(runner, mock_organizer):
    result = runner.invoke(organizer.organize_files, [RESOURCE_DIR])
    assert result.exit_code == 0

    log_message = _cleanup_abs_paths(result)
    assert log_message == (
        "Creating folder tests/resources/images\n"
        "Moving pic1.jpg to tests/resources/images\n"
        "Creating folder tests/resources/images\n"
        "Moving pic.png to tests/resources/images\n"
        "Skipping .hidden_file.md\n"
        "Creating folder tests/resources/music\n"
        "Moving audio1.wav to tests/resources/music\n"
        "Creating folder tests/resources/other\n"
        "Moving smth.md to tests/resources/other\n"
        "Creating folder tests/resources/videos\n"
        "Moving video.mp4 to tests/resources/videos\n"
        "Creating folder tests/resources/docs\n"
        "Moving file.txt to tests/resources/docs\n"
        "Creating folder tests/resources/books\n"
        "Moving file1.pdf to tests/resources/books\n"
    )


def test_organize_files_recursively(runner, mock_organizer):
    result = runner.invoke(organizer.organize_files_recursively, [RESOURCE_DIR])
    assert result.exit_code == 0

    log_message = _cleanup_abs_paths(result)
    assert log_message == (
        "----- Inside tests/resources/ -----\n"
        "Creating folder tests/resources/images\n"
        "Moving pic1.jpg to tests/resources/images\n"
        "Creating folder tests/resources/images\n"
        "Moving pic.png to tests/resources/images\n"
        "Skipping .hidden_file.md\n"
        "Skipping .hidden_other directory\n"
        "Creating folder tests/resources/music\n"
        "Moving audio1.wav to tests/resources/music\n"
        "Creating folder tests/resources/other\n"
        "Moving smth.md to tests/resources/other\n"
        "Creating folder tests/resources/videos\n"
        "Moving video.mp4 to tests/resources/videos\n"
        "Creating folder tests/resources/docs\n"
        "Moving file.txt to tests/resources/docs\n"
        "Creating folder tests/resources/books\n"
        "Moving file1.pdf to tests/resources/books\n"
        "----- Inside tests/resources/inner_test -----\n"
        "Creating folder tests/resources/inner_test/books\n"
        "Moving inner_file1.pdf to tests/resources/inner_test/books\n"
        "Creating folder tests/resources/inner_test/images\n"
        "Moving inner_pic.png to tests/resources/inner_test/images\n"
        "Creating folder tests/resources/inner_test/docs\n"
        "Moving inner_file.txt to tests/resources/inner_test/docs\n"
        "Creating folder tests/resources/inner_test/other\n"
        "Moving inner_smth.md to tests/resources/inner_test/other\n"
        "Skipping .inner_hidden_alone.wav\n"
        "Skipping .inner_hidden directory\n"
        "Creating folder tests/resources/inner_test/music\n"
        "Moving inner_audio1.wav to tests/resources/inner_test/music\n"
        "Creating folder tests/resources/inner_test/videos\n"
        "Moving inner_audio.mp4 to tests/resources/inner_test/videos\n"
        "Creating folder tests/resources/inner_test/images\n"
        "Moving inner_pic1.jpg to tests/resources/inner_test/images\n"
        "----- Inside tests/resources/inner_test/most_inner_test -----\n"
        "Creating folder tests/resources/inner_test/most_inner_test/books\n"
        "Moving most_inner_file1.pdf to tests/resources/inner_test/most_inner_test/books\n"
        "Creating folder tests/resources/inner_test/most_inner_test/docs\n"
        "Moving most_inner_file.txt to tests/resources/inner_test/most_inner_test/docs\n"
        "Creating folder tests/resources/inner_test/most_inner_test/images\n"
        "Moving most_inner_pic1.jpg to tests/resources/inner_test/most_inner_test/images\n"
        "Creating folder tests/resources/inner_test/most_inner_test/videos\n"
        "Moving most_inner_audio.mp4 to tests/resources/inner_test/most_inner_test/videos\n"
        "Moving most_inner_audio1.wav to tests/resources/inner_test/most_inner_test/music\n"
        "Creating folder tests/resources/inner_test/most_inner_test/images\n"
        "Moving most_inner_pic.png to tests/resources/inner_test/most_inner_test/images\n"
        "Creating folder tests/resources/inner_test/most_inner_test/other\n"
        "Moving most_inner_smth.md to tests/resources/inner_test/most_inner_test/other\n"
        "----- Inside tests/resources/inner_test/most_inner_test/music -----\n"
        "Creating folder tests/resources/inner_test/most_inner_test/music/music\n"
        "Moving inside_most_inner_audio.wav to tests/resources/inner_test/most_inner_test/music/music\n"
    )


def test_organize_files_recursively_and_flatten_folder(runner, mock_organizer):
    result = runner.invoke(organizer.organize_files_recursively, [RESOURCE_DIR, "--flat"])
    assert result.exit_code == 0

    log_message = _cleanup_abs_paths(result)
    assert log_message == (
        "----- Inside tests/resources/ -----\n"
        "Creating folder tests/resources/images\n"
        "Moving pic1.jpg to tests/resources/images\n"
        "Creating folder tests/resources/images\n"
        "Moving pic.png to tests/resources/images\n"
        "Moving .hidden_file.md to root directory\n"
        "Moving .hidden_other directory without stepping inside\n"
        "Creating folder tests/resources/music\n"
        "Moving audio1.wav to tests/resources/music\n"
        "Creating folder tests/resources/other\n"
        "Moving smth.md to tests/resources/other\n"
        "Creating folder tests/resources/videos\n"
        "Moving video.mp4 to tests/resources/videos\n"
        "Creating folder tests/resources/docs\n"
        "Moving file.txt to tests/resources/docs\n"
        "Creating folder tests/resources/books\n"
        "Moving file1.pdf to tests/resources/books\n"
        "----- Inside tests/resources/inner_test -----\n"
        "Creating folder tests/resources/books\n"
        "Moving inner_file1.pdf to tests/resources/books\n"
        "Creating folder tests/resources/images\n"
        "Moving inner_pic.png to tests/resources/images\n"
        "Creating folder tests/resources/docs\n"
        "Moving inner_file.txt to tests/resources/docs\n"
        "Creating folder tests/resources/other\n"
        "Moving inner_smth.md to tests/resources/other\n"
        "Moving .inner_hidden_alone.wav to root directory\n"
        "Moving .inner_hidden directory without stepping inside\n"
        "Creating folder tests/resources/music\n"
        "Moving inner_audio1.wav to tests/resources/music\n"
        "Creating folder tests/resources/videos\n"
        "Moving inner_audio.mp4 to tests/resources/videos\n"
        "Creating folder tests/resources/images\n"
        "Moving inner_pic1.jpg to tests/resources/images\n"
        "----- Inside tests/resources/inner_test/most_inner_test -----\n"
        "Creating folder tests/resources/books\n"
        "Moving most_inner_file1.pdf to tests/resources/books\n"
        "Creating folder tests/resources/docs\n"
        "Moving most_inner_file.txt to tests/resources/docs\n"
        "Creating folder tests/resources/images\n"
        "Moving most_inner_pic1.jpg to tests/resources/images\n"
        "Creating folder tests/resources/videos\n"
        "Moving most_inner_audio.mp4 to tests/resources/videos\n"
        "Creating folder tests/resources/music\n"
        "Moving most_inner_audio1.wav to tests/resources/music\n"
        "Creating folder tests/resources/images\n"
        "Moving most_inner_pic.png to tests/resources/images\n"
        "Creating folder tests/resources/other\n"
        "Moving most_inner_smth.md to tests/resources/other\n"
        "----- Inside tests/resources/inner_test/most_inner_test/music -----\n"
        "Creating folder tests/resources/music\nMoving inside_most_inner_audio.wav to tests/resources/music\n"
        "Removing tests/resources/inner_test/most_inner_test/music\n"
        "Removing tests/resources/inner_test/most_inner_test\n"
        "Removing tests/resources/inner_test\n"
    )


def _cleanup_abs_paths(result):
    resources_full_path = os.path.abspath(RESOURCE_DIR)
    log_message = result.output.replace(resources_full_path, RESOURCE_DIR)
    return log_message
