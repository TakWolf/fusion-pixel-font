import random

from configs.download_config import DownloadConfig, DownloadAssetConfig
from configs.dump_config import DumpConfig
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

download_configs = [
    DownloadConfig(
        name='ark-pixel',
        repository_name='TakWolf/ark-pixel-font',
        tag_name=None,
        asset_configs=[
            DownloadAssetConfig(
                file_name='ark-pixel-font-10px-monospaced-woff2-v{version}.zip',
                copy_list=[
                    ('ark-pixel-10px-monospaced-zh_cn.woff2', 'ark-pixel-10px-monospaced-zh_cn.woff2'),
                    ('OFL.txt', 'LICENSE.txt'),
                ],
            ),
            DownloadAssetConfig(
                file_name='ark-pixel-font-10px-proportional-woff2-v{version}.zip',
                copy_list=[
                    ('ark-pixel-10px-proportional-zh_cn.woff2', 'ark-pixel-10px-proportional-zh_cn.woff2'),
                ],
            ),
            DownloadAssetConfig(
                file_name='ark-pixel-font-12px-monospaced-woff2-v{version}.zip',
                copy_list=[
                    ('ark-pixel-12px-monospaced-zh_cn.woff2', 'ark-pixel-12px-monospaced-zh_cn.woff2'),
                ],
            ),
            DownloadAssetConfig(
                file_name='ark-pixel-font-12px-proportional-woff2-v{version}.zip',
                copy_list=[
                    ('ark-pixel-12px-proportional-zh_cn.woff2', 'ark-pixel-12px-proportional-zh_cn.woff2'),
                ],
            ),
        ],
    ),
    DownloadConfig(
        name='chill-bitmap',
        repository_name='Warren2060/Chill-Bitmap',
        tag_name=None,
        asset_configs=[
            DownloadAssetConfig(
                file_name='ChillBitmap7x_v{version}.zip',
                copy_list=[
                    ('ChillBitmap7x.woff2', 'ChillBitmap7x.woff2'),
                    ('License.txt', 'LICENSE.txt'),
                ],
            ),
        ],
    ),
    DownloadConfig(
        name='boutique-bitmap-9x9',
        repository_name='scott0107000/BoutiqueBitmap9x9',
        tag_name=None,
        asset_configs=[
            DownloadAssetConfig(
                file_name='BoutiqueBitmap9x9.zip',
                copy_list=[
                    ('BoutiqueBitmap9x9_{version}.ttf', 'BoutiqueBitmap9x9_{version}.ttf'),
                    ('OFL.txt', 'LICENSE.txt'),
                ],
            ),
        ],
    ),
    DownloadConfig(
        name='cubic-11',
        repository_name='ACh-K/Cubic-11',
        tag_name=None,
        asset_configs=[
            DownloadAssetConfig(
                file_name='Cubic_11.zip',
                copy_list=[
                    ('fonts/web/Cubic_11_{version}_R.woff2', 'Cubic_11_{version}_R.woff2'),
                    ('OFL.txt', 'LICENSE.txt'),
                ],
            ),
        ],
    ),
    DownloadConfig(
        name='galmuri',
        repository_name='quiple/galmuri',
        tag_name=None,
        asset_configs=[
            DownloadAssetConfig(
                file_name='Galmuri-v{version}.zip',
                copy_list=[
                    ('dist/Galmuri7.ttf', 'Galmuri7.ttf'),
                    ('dist/Galmuri9.ttf', 'Galmuri9.ttf'),
                    ('dist/Galmuri11.ttf', 'Galmuri11.ttf'),
                    ('dist/GalmuriMono7.ttf', 'GalmuriMono7.ttf'),
                    ('dist/GalmuriMono9.ttf', 'GalmuriMono9.ttf'),
                    ('dist/GalmuriMono11.ttf', 'GalmuriMono11.ttf'),
                    ('dist/LICENSE.txt', 'LICENSE.txt'),
                ],
            ),
        ],
    ),
]

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
    'zfull': [
        DumpConfig(
            font_file_name='Zfull-GB.ttf',
            font_size=10,
            width_mode_dir_name='common',
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
        'zfull',
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
