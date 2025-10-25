import pytest
from pathlib import Path

@pytest.fixture
def assets_dir():
    return Path(__file__).parent.parent / "tests" / "assets"
