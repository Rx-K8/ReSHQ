import pytest

from reshq.io.utils import make_directory


class TestMakeDirectory:
    def test_make_directory(self, tmp_path):
        temp_dir = tmp_path / "test"
        assert not temp_dir.is_dir()
        make_directory(temp_dir)
        assert temp_dir.is_dir()
