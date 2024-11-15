from pathlib import Path


def make_directory(dirpath: Path) -> None:
    dirpath.mkdir(parents=True, exist_ok=True)
