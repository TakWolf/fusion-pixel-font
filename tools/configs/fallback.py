import yaml

from tools.configs import path_define, options
from tools.configs.options import FontSize, LanguageFileFlavor


class FallbackConfig:
    @staticmethod
    def load() -> dict[FontSize, list[FallbackConfig]]:
        data = yaml.safe_load(path_define.configs_dir.joinpath('fallback.yaml').read_bytes())
        fallback_configs = {font_size: [] for font_size in options.font_sizes}
        for config_data in data:
            font_size = config_data['font-size']
            dir_from = config_data['dir-from']
            width_mode_dir_name = config_data['width-mode-dir-name']
            flavors = config_data.get('flavors', None)
            fallback_configs[font_size].append(FallbackConfig(
                font_size,
                dir_from,
                width_mode_dir_name,
                flavors.split(',') if flavors is not None else None,
            ))
        return fallback_configs

    font_size: FontSize
    dir_from: str
    width_mode_dir_name: str
    flavors: list[LanguageFileFlavor] | None

    def __init__(
            self,
            font_size: FontSize,
            dir_from: str,
            width_mode_dir_name: str,
            flavors: list[LanguageFileFlavor] | None,
    ):
        self.font_size = font_size
        self.dir_from = dir_from
        self.width_mode_dir_name = width_mode_dir_name
        self.flavors = flavors
