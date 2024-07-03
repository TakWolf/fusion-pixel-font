from pathlib import Path

from tools import configs
from tools.configs import path_define
from tools.utils import fs_util


class FallbackConfig:
    @staticmethod
    def load_all() -> dict[int, list['FallbackConfig']]:
        configs_data = fs_util.read_yaml(path_define.assets_dir.joinpath('fallback-configs.yml'))
        fallback_configs = {font_size: [] for font_size in configs.font_sizes}
        for config_data in configs_data:
            font_size = config_data['font-size']
            dir_from = path_define.dump_dir.joinpath(str(font_size), config_data['dir-from'])
            dir_to = path_define.fallback_glyphs_dir.joinpath(str(font_size), config_data['dir-to'])
            flavor = config_data.get('flavor', None)
            fallback_configs[font_size].append(FallbackConfig(
                font_size,
                dir_from,
                dir_to,
                flavor,
            ))
        return fallback_configs

    font_size: int
    dir_from: Path
    dir_to: Path
    flavor: str | None

    def __init__(
            self,
            font_size: int,
            dir_from: Path,
            dir_to: Path,
            flavor: str | None,
    ):
        self.font_size = font_size
        self.dir_from = dir_from
        self.dir_to = dir_to
        self.flavor = flavor
