import os

import yaml

from configs import path_define


class DownloadAssetConfig:
    def __init__(self, config_data: dict):
        self.file_name: str = config_data['file-name']
        self.copy_list: list[tuple[str, str]] = [(from_path, to_path) for from_path, to_path in config_data['copy-list'].items()]


class UpdateConfig:
    @staticmethod
    def load() -> list['UpdateConfig']:
        file_path = os.path.join(path_define.fonts_dir, 'update-configs.yaml')
        with open(file_path, 'rb') as file:
            configs_data: dict = yaml.safe_load(file)
        return [UpdateConfig(config_data) for config_data in configs_data]

    def __init__(self, config_data: dict):
        self.name: str = config_data['name']
        self.repository_name: str = config_data['repository-name']
        self.tag_name: str | None = config_data['tag-name']
        self.asset_configs = [DownloadAssetConfig(item_config_data) for item_config_data in config_data['asset-configs']]
