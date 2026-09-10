from pixel_font_knife import glyph_mapping_util
from pixel_font_knife.kerning_util import KerningConfig

from tools.configs import path_define, options
from tools.configs.dump import DumpConfig
from tools.configs.fallback import FallbackConfig
from tools.configs.font import FontConfig
from tools.configs.upgrade import UpgradeConfig

VERSION = '2026.09.01'

UPGRADE_CONFIGS = UpgradeConfig.load()

DUMP_CONFIGS = DumpConfig.load()

FALLBACK_CONFIGS = FallbackConfig.load()

FONT_CONFIGS = {font_size: FontConfig.load(font_size) for font_size in options.FONT_SIZES}

MAPPINGS = [
    glyph_mapping_util.load_mapping(path_define.MAPPINGS_DIR.joinpath('0080-00FF Latin-1 Supplement.yaml')),
    glyph_mapping_util.load_mapping(path_define.MAPPINGS_DIR.joinpath('2E80-2EFF CJK Radicals Supplement.yaml')),
    glyph_mapping_util.load_mapping(path_define.MAPPINGS_DIR.joinpath('2F00-2FDF Kangxi Radicals.yaml')),
]

KERNING_CONFIG = KerningConfig.load(path_define.KERNINGS_DIR.joinpath('default.yaml'))

LICENSE_CONFIGS = {
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

LOCALE_TO_LANGUAGE_FLAVOR = {
    'en': 'latin',
    'zh-hans': 'zh_hans',
    'zh-hant': 'zh_hant',
    'ja': 'ja',
    'ko': 'ko',
}
