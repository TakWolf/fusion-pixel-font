import yaml

from tools.config import path_define, options
from tools.config.options import FontSize, GlyphScope, LanguageFlavor


class FallbackConfig:
    @staticmethod
    def load() -> dict[FontSize, list[FallbackConfig]]:
        data = yaml.safe_load(path_define.CONFIGS_DIR.joinpath('fallback.yaml').read_bytes())
        fallback_configs = {
            font_size: []
            for font_size in options.FONT_SIZES
        }
        for config_data in data:
            font_size = config_data['font-size']
            dir_from = config_data['dir-from']
            glyph_scope = config_data['glyph-scope']
            flavors = config_data.get('flavors', None)
            fallback_configs[font_size].append(FallbackConfig(
                font_size,
                dir_from,
                glyph_scope,
                flavors.split(',') if flavors is not None else None,
            ))
        return fallback_configs

    font_size: FontSize
    dir_from: str
    glyph_scope: GlyphScope
    flavors: list[LanguageFlavor] | None

    def __init__(
            self,
            font_size: FontSize,
            dir_from: str,
            glyph_scope: GlyphScope,
            flavors: list[LanguageFlavor] | None,
    ) -> None:
        self.font_size = font_size
        self.dir_from = dir_from
        self.glyph_scope = glyph_scope
        self.flavors = flavors
