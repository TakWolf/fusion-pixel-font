import json
import shutil
from pathlib import Path
from typing import Any

import yaml


def delete_dir(path: Path):
    if path.exists():
        shutil.rmtree(path)


def is_empty_dir(path: Path) -> bool:
    for item_path in path.iterdir():
        if item_path.name == '.DS_Store':
            continue
        return False
    return True


def read_json(path: Path) -> Any:
    return json.loads(path.read_text('utf-8'))


def write_json(data: Any, path: Path):
    path.write_text(f'{json.dumps(data, indent=2, ensure_ascii=False)}\n', 'utf-8')


def read_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text('utf-8'))
