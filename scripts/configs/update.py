import os

from scripts.configs import path_define
from scripts.utils import fs_util


class DownloadAssetConfig:
    def __init__(self, config_data: dict):
        self.file_name: str = config_data['file_name']
        self.copy_list: list[tuple[str, str]] = []
        for from_path, to_path in config_data['copy_list'].items():
            if to_path is None:
                to_path = from_path
            self.copy_list.append((from_path, to_path))


class UpdateConfig:
    @staticmethod
    def load() -> list['UpdateConfig']:
        file_path = os.path.join(path_define.assets_dir, 'update-configs.yaml')
        configs_data: dict = fs_util.read_yaml(file_path)
        return [UpdateConfig(config_data) for config_data in configs_data]

    def __init__(self, config_data: dict):
        self.name: str = config_data['name']
        self.repository_name: str = config_data['repository_name']
        self.tag_name: str | None = config_data['tag_name']
        self.asset_configs = [DownloadAssetConfig(item_data) for item_data in config_data['asset_configs']]
