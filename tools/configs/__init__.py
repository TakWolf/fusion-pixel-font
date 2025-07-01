from tools.configs import path_define

version = '2025.03.14'

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
