import json
import os
import shutil
import tomllib
from typing import Any

import yaml


def delete_dir(path: str | bytes | os.PathLike[str] | os.PathLike[bytes]):
    if os.path.exists(path):
        shutil.rmtree(path)


def read_str(path: str | bytes | os.PathLike[str] | os.PathLike[bytes]) -> str:
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()


def write_str(text: str, path: str | bytes | os.PathLike[str] | os.PathLike[bytes]):
    with open(path, 'w', encoding='utf-8') as file:
        file.write(text)


def read_json(path: str | bytes | os.PathLike[str] | os.PathLike[bytes]) -> Any:
    return json.loads(read_str(path))


def write_json(data: Any, path: str | bytes | os.PathLike[str] | os.PathLike[bytes]):
    write_str(f'{json.dumps(data, indent=2, ensure_ascii=False)}\n', path)


def read_toml(path: str | bytes | os.PathLike[str] | os.PathLike[bytes]) -> Any:
    return tomllib.loads(read_str(path))


def read_yaml(path: str | bytes | os.PathLike[str] | os.PathLike[bytes]) -> Any:
    return yaml.safe_load(read_str(path))
