from __future__ import annotations

from pathlib import Path

import yaml

from tools.configs import path_define, options
from tools.configs.options import FontSize, LanguageFileFlavor


class FallbackConfig:
    @staticmethod
    def load() -> dict[FontSize, list[FallbackConfig]]:
        configs_data = yaml.safe_load(path_define.assets_dir.joinpath('fallback-configs.yml').read_bytes())
        fallback_configs = {font_size: [] for font_size in options.font_sizes}
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

    font_size: FontSize
    dir_from: Path
    dir_to: Path
    flavor: LanguageFileFlavor | None

    def __init__(
            self,
            font_size: FontSize,
            dir_from: Path,
            dir_to: Path,
            flavor: LanguageFileFlavor | None,
    ):
        self.font_size = font_size
        self.dir_from = dir_from
        self.dir_to = dir_to
        self.flavor = flavor
