import shutil
from filecmp import dircmp
from os import path

import pytest
from click.testing import CliRunner


@pytest.fixture(scope="function")
def runner(request):
    return CliRunner()


@pytest.fixture(scope="session")
def tmp_dirs(tmp_path_factory):
    path = tmp_path_factory.mktemp("file-file_manager")
    shutil.copytree("./tests/resources/plain", path / "plain")
    shutil.copytree("./tests/resources/results/plain", path / "results/plain")
    return str(path / "plain"), str(path / "results/plain")


@pytest.fixture(scope="session")
def tmp_cmp_dirs(tmp_path_factory):
    path = tmp_path_factory.mktemp("file-file_manager")
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
def compare(source: str, target: str, include_hidden: bool = False) -> tuple[int, ...]:
    changed_files = {}
    deleted_files = {}
    added_files = {}

    _diff(dircmp(source, target), changed_files, deleted_files, added_files, include_hidden)
    return len(changed_files), len(deleted_files), len(added_files)


def _diff(
    cmp_obj: dircmp,
    changed_files: dict[str, int],
    deleted_files: dict[str, str],
    added_files: dict[str, str],
    include_hidden: bool,
) -> None:
    for changed_file in cmp_obj.diff_files:
        file1 = f"{cmp_obj.left}/{changed_file}"
        file2 = f"{cmp_obj.right}/{changed_file}"
        changed_files[file2] = path.getsize(file2) - path.getsize(file1)

    for deleted_file in cmp_obj.left_only:
        file1 = f"{cmp_obj.right}/{deleted_file}"
        deleted_files[file1] = "DELETED!"

    for added_file in cmp_obj.right_only:
        file1 = f"{cmp_obj.right}/{added_file}"
        added_files[file1] = "ADDED!"

    # TODO: only in the recursive version
    for sub_dir in cmp_obj.subdirs.values():
        _diff(sub_dir, changed_files, deleted_files, added_files, include_hidden)
