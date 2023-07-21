import json
import os

import yaml

import configs
from configs import path_define


class DumpConfig:
    @staticmethod
    def load() -> dict[int, list['DumpConfig']]:
        configs_file_path = os.path.join(path_define.fonts_dir, 'dump-configs.yaml')
        with open(configs_file_path, 'rb') as file:
            configs_data: dict = yaml.safe_load(file)
        font_size_to_dump_configs = {font_config.size: [] for font_config in configs.font_configs}
        for name, list_data in configs_data.items():
            version_file_path = os.path.join(path_define.fonts_dir, name, 'version.json')
            with open(version_file_path, 'r', encoding='utf-8') as file:
                version: str = json.loads(file.read())['version']
            for item_data in list_data:
                dump_config = DumpConfig(name, version, item_data)
                font_size_to_dump_configs[dump_config.font_size].append(dump_config)
        return font_size_to_dump_configs

    def __init__(self, name: str, version: str, config_data: dict):
        self.name = name
        self.font_file_path: str = os.path.join(path_define.fonts_dir, name, config_data['font-file-name'].format(version=version))
        self.font_size: int = config_data['font-size']
        self.dump_dir: str = os.path.join(path_define.dump_dir, str(self.font_size), config_data['dump-dir-name'])
        self.rasterize_size: int = config_data.get('rasterize-size', self.font_size)
        self.rasterize_offset_x: int = config_data.get('rasterize-offset-x', 0)
        self.rasterize_offset_y: int = config_data.get('rasterize-offset-y', 0)

    @property
    def rasterize_offset(self) -> tuple[int, int]:
        return self.rasterize_offset_x, self.rasterize_offset_y
