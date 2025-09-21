from __future__ import annotations

import json
from pathlib import Path

import yaml

from tools.configs import path_define, options
from tools.configs.options import FontSize


class DumpConfig:
    @staticmethod
    def load() -> dict[FontSize, list[DumpConfig]]:
        data = yaml.safe_load(path_define.configs_dir.joinpath('dump.yml').read_bytes())
        dump_configs = {font_size: [] for font_size in options.font_sizes}
        for name, items_data in data.items():
            version = json.loads(path_define.fonts_dir.joinpath(name, 'version.json').read_bytes())['version']
            for item_data in items_data:
                font_file_path = path_define.fonts_dir.joinpath(name, item_data['font-file-name'].format(version=version))
                font_size = item_data['font-size']
                dump_dir = path_define.dump_dir.joinpath(str(font_size), item_data['dump-dir-name'])
                rasterize_size = item_data.get('rasterize-size', font_size)
                rasterize_offset_x = item_data.get('rasterize-offset-x', 0)
                rasterize_offset_y = item_data.get('rasterize-offset-y', 0)
                dump_configs[font_size].append(DumpConfig(
                    name,
                    font_file_path,
                    font_size,
                    dump_dir,
                    rasterize_size,
                    rasterize_offset_x,
                    rasterize_offset_y,
                ))
        return dump_configs

    name: str
    font_file_path: Path
    font_size: FontSize
    dump_dir: Path
    rasterize_size: int
    rasterize_offset_x: int
    rasterize_offset_y: int

    def __init__(
            self,
            name: str,
            font_file_path: Path,
            font_size: FontSize,
            dump_dir: Path,
            rasterize_size: int,
            rasterize_offset_x: int,
            rasterize_offset_y: int,
    ):
        self.name = name
        self.font_file_path = font_file_path
        self.font_size = font_size
        self.dump_dir = dump_dir
        self.rasterize_size = rasterize_size
        self.rasterize_offset_x = rasterize_offset_x
        self.rasterize_offset_y = rasterize_offset_y

    @property
    def rasterize_offset(self) -> tuple[int, int]:
        return self.rasterize_offset_x, self.rasterize_offset_y
