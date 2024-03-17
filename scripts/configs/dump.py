import json
import os

from scripts import configs
from scripts.configs import path_define
from scripts.utils import fs_util


class DumpConfig:
    @staticmethod
    def load_all() -> dict[int, list['DumpConfig']]:
        configs_file_path = os.path.join(path_define.fonts_dir, 'dump-configs.yaml')
        configs_data: dict = fs_util.read_yaml(configs_file_path)
        dump_configs = {font_size: [] for font_size in configs.font_sizes}
        for name, list_data in configs_data.items():
            version_file_path = os.path.join(path_define.fonts_dir, name, 'version.json')
            version: str = json.loads(fs_util.read_str(version_file_path))['version']
            for item_data in list_data:
                dump_config = DumpConfig(name, version, item_data)
                dump_configs[dump_config.font_size].append(dump_config)
        return dump_configs

    def __init__(self, name: str, version: str, config_data: dict):
        self.name = name
        self.font_file_path: str = os.path.join(path_define.fonts_dir, name, config_data['font_file_name'].format(version=version))
        self.font_size: int = config_data['font_size']
        self.dump_dir: str = os.path.join(path_define.dump_dir, str(self.font_size), config_data['dump_dir_name'])
        self.rasterize_size: int = config_data.get('rasterize_size', self.font_size)
        self.rasterize_offset_x: int = config_data.get('rasterize_offset_x', 0)
        self.rasterize_offset_y: int = config_data.get('rasterize_offset_y', 0)

    @property
    def rasterize_offset(self) -> tuple[int, int]:
        return self.rasterize_offset_x, self.rasterize_offset_y
