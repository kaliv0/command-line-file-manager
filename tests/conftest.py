import shutil

import pytest
from click.testing import CliRunner


@pytest.fixture(scope="function")
def runner(request):
    return CliRunner()


@pytest.fixture(scope="session")
def tmp_dirs(tmp_path_factory):
    path = tmp_path_factory.mktemp("file-manager")
    shutil.copytree("./tests/resources/plain", path / "plain")
    shutil.copytree("./tests/resources/results/plain", path / "results/plain")
    return str(path / "plain"), str(path / "results/plain")


@pytest.fixture(scope="function")
def mock_organizer(monkeypatch):
    monkeypatch.setattr("shutil.move", lambda src, target: None)
    monkeypatch.setattr("os.makedirs", lambda target: None)
    monkeypatch.setattr("os.rmdir", lambda target: None)
    monkeypatch.setattr("os.remove", lambda target: None)
