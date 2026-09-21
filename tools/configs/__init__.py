from pixel_font_knife.cmap.kerning.template import CmapKerningTemplate
from pixel_font_knife.cmap.mapping.mapping import CmapMapping

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
    CmapMapping.load_yaml(
        path_define.CONFIGS_MAPPINGS_DIR.joinpath('0080-00FF Latin-1 Supplement.yaml'),
        allowed_flavors=options.LANGUAGE_FLAVORS,
    ),
    CmapMapping.load_yaml(
        path_define.CONFIGS_MAPPINGS_DIR.joinpath('2E80-2EFF CJK Radicals Supplement.yaml'),
        allowed_flavors=options.LANGUAGE_FLAVORS,
    ),
    CmapMapping.load_yaml(
        path_define.CONFIGS_MAPPINGS_DIR.joinpath('2F00-2FDF Kangxi Radicals.yaml'),
        allowed_flavors=options.LANGUAGE_FLAVORS,
    ),
    CmapMapping.load_yaml(
        path_define.CONFIGS_MAPPINGS_DIR.joinpath('F900-FAFF CJK Compatibility Ideographs.yaml'),
        allowed_flavors=options.LANGUAGE_FLAVORS,
    ),
]

KERNING_TEMPLATE_DEFAULT = CmapKerningTemplate.load(path_define.CONFIGS_KERNING_DIR.joinpath('default.yaml'))

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

LANGUAGE_FLAVOR_TO_FONT_NAME = {
    'latin': 'latin',
    'zh_hans': 'zh-Hans',
    'zh_hant': 'zh-Hant',
    'zh_hk': 'zh-HK',
    'zh_tw': 'zh-TW',
    'ja': 'ja',
    'ko': 'ko',
}

LANGUAGE_FLAVOR_TO_LOCALE = {
    'latin': 'en',
    'zh_hans': 'zh-Hans',
    'zh_hant': 'zh-Hant',
    'zh_hk': 'zh-Hant-HK',
    'zh_tw': 'zh-Hant-TW',
    'ja': 'ja',
    'ko': 'ko',
}
