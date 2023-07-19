import os

import yaml

from configs import path_define


class FallbackConfig:
    @staticmethod
    def load() -> list['FallbackConfig']:
        file_path = os.path.join(path_define.fonts_dir, 'fallback-configs.yaml')
        with open(file_path, 'rb') as file:
            configs_data: dict = yaml.safe_load(file)
        return [FallbackConfig(config_data) for config_data in configs_data]

    def __init__(self, config_data: dict):
        self.from_dir: str = config_data['from_dir']
        self.to_dir: str = config_data['to_dir']
        self.flavor: str | None = config_data.get('flavor', None)
