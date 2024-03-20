import os

from scripts import configs
from scripts.configs import path_define
from scripts.utils import fs_util


class FallbackConfig:
    @staticmethod
    def load_all() -> dict[int, list['FallbackConfig']]:
        file_path = os.path.join(path_define.assets_dir, 'fallback-configs.yaml')
        configs_data: dict = fs_util.read_yaml(file_path)
        fallback_configs = {font_size: [] for font_size in configs.font_sizes}
        for config_data in configs_data:
            fallback_config = FallbackConfig(config_data)
            fallback_configs[fallback_config.font_size].append(fallback_config)
        return fallback_configs

    def __init__(self, config_data: dict):
        self.font_size: int = config_data['font_size']
        self.dir_from: str = os.path.join(path_define.dump_dir, str(self.font_size), config_data['dir_from'])
        self.dir_to: str = os.path.join(path_define.fallback_glyphs_dir, str(self.font_size), config_data['dir_to'])
        self.flavor: str | None = config_data.get('flavor', None)
