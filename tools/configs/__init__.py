from typing import Literal, get_args

from tools.configs import path_define

version = '2025.03.14'

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
    'zh_cn',
    'zh_hk',
    'zh_tw',
    'zh_tr',
    'ja',
    'ko',
]
language_file_flavors = list[LanguageFileFlavor](get_args(LanguageFileFlavor.__value__))

type FontFormat = Literal['otf', 'otf.woff', 'otf.woff2', 'ttf', 'ttf.woff', 'ttf.woff2', 'otc', 'ttc', 'bdf', 'pcf']
font_formats = list[FontFormat](get_args(FontFormat.__value__))

font_single_formats = ['otf', 'otf.woff', 'otf.woff2', 'ttf', 'ttf.woff', 'ttf.woff2', 'bdf', 'pcf']
font_collection_formats = ['otc', 'ttc']

type Attachment = Literal[
    'release',
    'info',
    'alphabet',
    'html',
    'image',
]
attachments = list[Attachment](get_args(Attachment.__value__))

mapping_file_paths = [
    path_define.ark_pixel_mappings_dir.joinpath('2700-27BF Dingbats.yml'),
    path_define.ark_pixel_mappings_dir.joinpath('2E80-2EFF CJK Radicals Supplement.yml'),
    path_define.ark_pixel_mappings_dir.joinpath('2F00-2FDF Kangxi Radicals.yml'),
]

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
