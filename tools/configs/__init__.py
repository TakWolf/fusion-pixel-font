from tools.configs.source import GithubSourceConfig, GitSourceType

font_version = '2024.05.12'

font_sizes = [8, 10, 12]

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

font_formats = ['otf', 'woff2', 'ttf', 'bdf', 'pcf']

font_collection_formats = ['otc', 'ttc']

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

ark_pixel_config = GithubSourceConfig(
    repository_name='TakWolf/ark-pixel-font',
    source_type=GitSourceType.TAG,
    source_name=None,
)
