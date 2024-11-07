from typing import Literal, get_args

version = '2024.11.04'

type FontSize = Literal[8, 10, 12]
font_sizes = list[FontSize](get_args(FontSize.__value__))

type WidthMode = Literal[
    'monospaced',
    'proportional',
]
width_modes = list[WidthMode](get_args(WidthMode.__value__))

type LanguageFlavor = Literal[
    'latin',
    'zh_hans',
    'zh_hant',
    'ja',
    'ko',
]
language_flavors = list[LanguageFlavor](get_args(LanguageFlavor.__value__))

type LanguageFileFlavor = Literal[
    'latin',
    'zh_cn',
    'zh_hk',
    'zh_tw',
    'zh_tr',
    'ja',
    'ko',
]
language_file_flavors = list[LanguageFileFlavor](get_args(LanguageFileFlavor.__value__))

type FontFormat = Literal['otf', 'ttf', 'woff2', 'bdf', 'pcf', 'otc', 'ttc']
font_formats = list[FontFormat](get_args(FontFormat.__value__))

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
