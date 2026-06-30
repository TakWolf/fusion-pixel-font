from pixel_font_knife import glyph_mapping_util
from pixel_font_knife.kerning_util import KerningConfig

from tools.configs import path_define, options
from tools.configs.dump import DumpConfig
from tools.configs.fallback import FallbackConfig
from tools.configs.font import FontConfig
from tools.configs.upgrade import UpgradeConfig

version = '2026.07.01'

upgrade_configs = UpgradeConfig.load()

dump_configs = DumpConfig.load()

fallback_configs = FallbackConfig.load()

font_configs = {font_size: FontConfig.load(font_size) for font_size in options.font_sizes}

mappings = [
    glyph_mapping_util.load_mapping(path_define.mappings_dir.joinpath('2E80-2EFF CJK Radicals Supplement.yml')),
    glyph_mapping_util.load_mapping(path_define.mappings_dir.joinpath('2F00-2FDF Kangxi Radicals.yml')),
]

kerning_config = KerningConfig.load(path_define.kernings_dir.joinpath('default.yml'))

license_configs = {
    8: {
        'misaki': [
            'misaki.txt',
        ],
        'miseki-bitmap': [
            'LICENSE.txt',
        ],
        'boutique-bitmap-7x7': [
            'OFL.txt',
        ],
        'galmuri': [
            'LICENSE.txt',
        ],
    },
    10: {
        'ark-pixel': [
            'OFL.txt',
        ],
        'boutique-bitmap-9x9': [
            'OFL.txt',
        ],
        'galmuri': [
            'LICENSE.txt',
        ],
    },
    12: {
        'ark-pixel': [
            'OFL.txt',
        ],
        'cubic-11': [
            'OFL.txt',
        ],
        'galmuri': [
            'LICENSE.txt',
        ],
    },
}

locale_to_language_flavor = {
    'en': 'latin',
    'zh-hans': 'zh_hans',
    'zh-hant': 'zh_hant',
    'ja': 'ja',
    'ko': 'ko',
}
