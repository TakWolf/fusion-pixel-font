from tools.configs import path_define
from tools.utils import fs_util


class DownloadAssetConfig:
    file_name: str | None
    copy_list: list[tuple[str, str]]

    def __init__(self, file_name: str | None, copy_list: list[tuple[str, str]]):
        self.file_name = file_name
        self.copy_list = copy_list


class UpdateConfig:
    @staticmethod
    def load_all() -> list['UpdateConfig']:
        configs_data = fs_util.read_yaml(path_define.assets_dir.joinpath('update-configs.yaml'))
        update_configs = []
        for config_data in configs_data:
            name = config_data['name']
            repository_name = config_data['repository_name']
            tag_name = config_data['tag_name']
            asset_configs = []
            for asset_data in config_data['asset_configs']:
                file_name = asset_data.get('file_name', None)
                copy_list = []
                for from_path, to_path in asset_data['copy_list'].items():
                    if to_path is None:
                        to_path = from_path
                    copy_list.append((from_path, to_path))
                asset_configs.append(DownloadAssetConfig(file_name, copy_list))
            update_configs.append(UpdateConfig(name, repository_name, tag_name, asset_configs))
        return update_configs

    name: str
    repository_name: str
    tag_name: str | None
    asset_configs: list[DownloadAssetConfig]

    def __init__(
            self,
            name: str,
            repository_name: str,
            tag_name: str | None,
            asset_configs: list[DownloadAssetConfig],
    ):
        self.name = name
        self.repository_name = repository_name
        self.tag_name = tag_name
        self.asset_configs = asset_configs
