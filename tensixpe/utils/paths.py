from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def ronin_path(ronin_home: str | Path = "external/ronin") -> Path:
    p = Path(ronin_home)
    return p if p.is_absolute() else repo_root() / p
