import random

from scripts.configs.dump_config import DumpConfig
from scripts.configs.fallback_config import FallbackConfig
from scripts.configs.font_config import FontConfig
from scripts.configs.git_deploy_config import GitDeployConfig

build_random_key = random.random()

width_modes = [
    'monospaced',
    'proportional',
]

language_file_flavors = [
    'latin',
    'zh_cn',
    'zh_hk',
    'zh_tw',
    'zh_tr',
    'ja',
    'ko',
]

language_flavors = [
    'latin',
    'zh_hans',
    'zh_hant',
    'ja',
    'ko',
]

locale_to_language_flavor = {
    'en': 'latin',
    'zh-hans': 'zh_hans',
    'zh-hant': 'zh_hant',
    'ja': 'ja',
    'ko': 'ko',
}

font_formats = ['otf', 'woff2', 'ttf', 'bdf']

font_collection_formats = ['otc', 'ttc']

font_configs = [FontConfig(size) for size in [8, 10, 12]]
font_size_to_config = {font_config.size: font_config for font_config in font_configs}

font_size_to_dump_configs = DumpConfig.load()

font_size_to_fallback_configs = FallbackConfig.load()

font_size_to_license_configs = {
    8: [
        'misaki',
        'chill-bitmap',
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

git_deploy_configs = [GitDeployConfig(
    url='git@github.com:TakWolf/fusion-pixel-font.git',
    remote_name='github',
    branch_name='gh-pages',
)]