import random

from configs.font_config import FontConfig
from configs.git_deploy_config import GitDeployConfig

build_random_key = random.random()

font_configs = [FontConfig(size) for size in [8, 10, 12]]
font_size_to_config: dict[int, FontConfig] = {font_config.size: font_config for font_config in font_configs}

width_modes = [
    'monospaced',
    'proportional',
]

width_mode_dir_names = [
    'common',
    'monospaced',
    'proportional',
]

font_formats = ['otf', 'woff2', 'ttf', 'bdf']

font_size_to_fallback_names = {
    8: [
        'chill-bitmap',
        'misaki',
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
