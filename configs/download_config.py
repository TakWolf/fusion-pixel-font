
class DownloadAssetConfig:
    def __init__(
            self,
            file_name: str,
            copy_list: list[tuple[str, str]],
    ):
        self.file_name = file_name
        self.copy_list = copy_list


class DownloadConfig:
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
