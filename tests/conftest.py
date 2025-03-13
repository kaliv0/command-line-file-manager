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


@pytest.fixture(scope="session")
def tmp_cmp_dirs(tmp_path_factory):
    path = tmp_path_factory.mktemp("file-manager")
    shutil.copytree("./tests/resources/plain", path / "plain")
    shutil.copytree("./tests/resources/results/plain_modified", path / "results/plain_modified")
    return str(path / "plain"), str(path / "results/plain_modified")


@pytest.fixture(scope="function")
def mock_organizer(monkeypatch):
    monkeypatch.setattr("shutil.move", lambda src, target: None)
    monkeypatch.setattr("os.makedirs", lambda target: None)
    monkeypatch.setattr("os.rmdir", lambda target: None)
    monkeypatch.setattr("os.remove", lambda target: None)


# ### helpers ###
def compare(source: str, target: str) -> tuple[int, ...]:
    from filecmp import dircmp
    from manager.utils.scanner import diff_report

    changed_files = {}
    deleted_files = {}
    added_files = {}

    diff_report(dircmp(source, target), changed_files, deleted_files, added_files)
    return len(changed_files), len(deleted_files), len(added_files)
