import os

from scripts import configs
from scripts.configs import path_define
from scripts.utils import fs_util


class FallbackConfig:
    @staticmethod
    def load_all() -> dict[int, list['FallbackConfig']]:
        configs_data = fs_util.read_yaml(os.path.join(path_define.assets_dir, 'fallback-configs.yaml'))
        fallback_configs = {font_size: [] for font_size in configs.font_sizes}
        for config_data in configs_data:
            font_size = config_data['font_size']
            dir_from = os.path.join(path_define.dump_dir, str(font_size), config_data['dir_from'])
            dir_to = os.path.join(path_define.fallback_glyphs_dir, str(font_size), config_data['dir_to'])
            flavor = config_data.get('flavor', None)
            fallback_configs[font_size].append(FallbackConfig(
                font_size,
                dir_from,
                dir_to,
                flavor,
            ))
        return fallback_configs

    def __init__(
            self,
            font_size: int,
            dir_from: str,
            dir_to: str,
            flavor: str | None,
    ):
        self.font_size = font_size
        self.dir_from = dir_from
        self.dir_to = dir_to
        self.flavor = flavor
