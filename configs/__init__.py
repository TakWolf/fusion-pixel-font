import random

from configs.dump_config import DumpConfig
from configs.font_config import FontConfig
from configs.git_deploy_config import GitDeployConfig
from configs.update_config import UpdateConfig

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

name_to_dump_configs = {
    'ark-pixel': [
        DumpConfig(
            font_file_name='ark-pixel-10px-monospaced-zh_cn.woff2',
            font_size=10,
            width_mode_dir_name='monospaced',
        ),
        DumpConfig(
            font_file_name='ark-pixel-10px-proportional-zh_cn.woff2',
            font_size=10,
            width_mode_dir_name='proportional',
        ),
        DumpConfig(
            font_file_name='ark-pixel-12px-monospaced-zh_cn.woff2',
            font_size=12,
            width_mode_dir_name='monospaced',
        ),
        DumpConfig(
            font_file_name='ark-pixel-12px-proportional-zh_cn.woff2',
            font_size=12,
            width_mode_dir_name='proportional',
        ),
    ],
    'misaki': [
        DumpConfig(
            font_file_name='misaki_gothic.ttf',
            font_size=8,
            width_mode_dir_name='common',
            rasterize_offset=(0, 1),
        ),
    ],
    'chill-bitmap': [
        DumpConfig(
            font_file_name='ChillBitmap7x.woff2',
            font_size=8,
            width_mode_dir_name='common',
            rasterize_offset=(0, 1),
        ),
    ],
    'boutique-bitmap-9x9': [
        DumpConfig(
            font_file_name='BoutiqueBitmap9x9_{version}.ttf',
            font_size=10,
            width_mode_dir_name='common',
            rasterize_offset=(0, 1),
        ),
    ],
    'cubic-11': [
        DumpConfig(
            font_file_name='Cubic_11_{version}_R.woff2',
            font_size=12,
            width_mode_dir_name='common',
            rasterize_offset=(-1, 1),
        ),
    ],
    'galmuri': [
        DumpConfig(
            font_file_name='Galmuri7.ttf',
            font_size=8,
            width_mode_dir_name='proportional',
            rasterize_offset=(0, 1),
        ),
        DumpConfig(
            font_file_name='Galmuri9.ttf',
            font_size=10,
            width_mode_dir_name='proportional',
            rasterize_offset=(0, 1),
        ),
        DumpConfig(
            font_file_name='Galmuri11.ttf',
            font_size=12,
            width_mode_dir_name='proportional',
            rasterize_offset=(0, 1),
        ),
        DumpConfig(
            font_file_name='GalmuriMono7.ttf',
            font_size=8,
            width_mode_dir_name='monospaced',
            rasterize_offset=(0, 1),
        ),
        DumpConfig(
            font_file_name='GalmuriMono9.ttf',
            font_size=10,
            width_mode_dir_name='monospaced',
            rasterize_offset=(0, 1),
        ),
        DumpConfig(
            font_file_name='GalmuriMono11.ttf',
            font_size=12,
            width_mode_dir_name='monospaced',
            rasterize_offset=(0, 1),
        ),
    ],
}

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
