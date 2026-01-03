from pixel_font_knife import glyph_mapping_util
from pixel_font_knife.kerning_util import KerningConfig

from tools.configs import path_define, options
from tools.configs.dump import DumpConfig
from tools.configs.fallback import FallbackConfig
from tools.configs.font import FontConfig
from tools.configs.upgrade import UpgradeConfig

version = '2026.01.04'

font_configs = {font_size: FontConfig.load(font_size) for font_size in options.font_sizes}

mappings = [
    glyph_mapping_util.load_mapping(path_define.mappings_dir.joinpath('2700-27BF Dingbats.yml')),
    glyph_mapping_util.load_mapping(path_define.mappings_dir.joinpath('2E80-2EFF CJK Radicals Supplement.yml')),
    glyph_mapping_util.load_mapping(path_define.mappings_dir.joinpath('2F00-2FDF Kangxi Radicals.yml')),
    glyph_mapping_util.load_mapping(path_define.mappings_dir.joinpath('1F100-1F1FF Enclosed Alphanumeric Supplement.yml')),
]

kerning_config = KerningConfig.load(path_define.kernings_dir.joinpath('default.yml'))

license_configs = {
    8: [
        'misaki',
        'miseki-bitmap',
        'boutique-bitmap-7x7',
        'galmuri',
    ],
    10: [
        'ark-pixel',
        'boutique-bitmap-9x9',
        'galmuri',
    ],
    12: [
        'ark-pixel',
        'cubic-11',
        'galmuri',
    ],
}

locale_to_language_flavor = {
    'en': 'latin',
    'zh-hans': 'zh_hans',
    'zh-hant': 'zh_hant',
    'ja': 'ja',
    'ko': 'ko',
}
