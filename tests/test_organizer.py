import os

from app.utils import organizer
from tests.conftest import RESOURCE_DIR


def test_organize_files(runner, monkeypatch):
    monkeypatch.setattr("shutil.move", lambda src, target: None)
    monkeypatch.setattr("os.makedirs", lambda target: None)
    result = runner.invoke(organizer.organize_files, [RESOURCE_DIR])
    assert result.exit_code == 0

    # clean up of absolute directory paths in the log messages
    resources_full_path = os.path.abspath(RESOURCE_DIR)
    log_message = result.output.replace(resources_full_path, RESOURCE_DIR)
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
