import logging
import os

import configs
from configs import path_define
from utils import fs_util

logger = logging.getLogger('design-service')


def collect_glyph_files(width_mode):
    alphabet = set()
    glyph_file_paths = {}
    fallback_infos = {'ark-pixel': set()}
    glyphs_dir_infos = [
        ('ark-pixel', os.path.join(path_define.assets_dir, 'glyphs')),
        ('ark-pixel', os.path.join(path_define.dump_dir, f'ark-pixel-{width_mode}')),
    ]
    for fallback_name in configs.fallback_names:
        fallback_infos[fallback_name] = set()
        glyphs_dir = os.path.join(path_define.dump_dir, fallback_name)
        glyphs_dir_infos.append((fallback_name, glyphs_dir))
    for fallback_name, glyphs_dir in glyphs_dir_infos:
        if not os.path.isdir(glyphs_dir):
            continue
        for glyph_file_dir, glyph_file_name in fs_util.walk_files(glyphs_dir):
            if not glyph_file_name.endswith('.png'):
                continue
            glyph_file_path = os.path.join(glyph_file_dir, glyph_file_name)
            if glyph_file_name == 'notdef.png':
                if '.notdef' not in glyph_file_paths:
                    glyph_file_paths['.notdef'] = glyph_file_path
            else:
                uni_hex_name = glyph_file_name.removesuffix('.png').upper()
                code_point = int(uni_hex_name, 16)
                if code_point not in glyph_file_paths:
                    glyph_file_paths[code_point] = glyph_file_path
                    c = chr(code_point)
                    alphabet.add(c)
                    fallback_infos[fallback_name].add(c)
    alphabet = list(alphabet)
    alphabet.sort()
    return alphabet, glyph_file_paths, fallback_infos
