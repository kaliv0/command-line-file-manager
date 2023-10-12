import pytest

from click.testing import CliRunner

RESOURCE_DIR = "tests/resources"


@pytest.fixture(scope="function")
def runner(request):
    return CliRunner()
