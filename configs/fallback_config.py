import os

import yaml

import configs
from configs import path_define


class FallbackConfig:
    @staticmethod
    def load() -> dict[int, list['FallbackConfig']]:
        file_path = os.path.join(path_define.fonts_dir, 'fallback-configs.yaml')
        with open(file_path, 'rb') as file:
            configs_data: dict = yaml.safe_load(file)
        font_size_to_fallback_configs = {font_config.size: [] for font_config in configs.font_configs}
        for config_data in configs_data:
            fallback_config = FallbackConfig(config_data)
            font_size_to_fallback_configs[fallback_config.font_size].append(fallback_config)
        return font_size_to_fallback_configs

    def __init__(self, config_data: dict):
        self.font_size: int = config_data['font_size']
        self.from_dir: str = os.path.join(path_define.dump_dir, str(self.font_size), config_data['from_dir'])
        self.to_dir: str = os.path.join(path_define.fallback_glyphs_dir, str(self.font_size), config_data['to_dir'])
        self.flavor: str | None = config_data.get('flavor', None)
