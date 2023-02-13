import logging
import math
import os

from PIL import ImageFont, Image, ImageDraw
from fontTools.ttLib import TTFont

import configs
from configs import path_define
from utils import fs_util, glyph_util

logger = logging.getLogger('dump-service')


def dump_font(dump_config):
    dump_dir = os.path.join(path_define.dump_dir, dump_config.name)
    fs_util.make_dirs_if_not_exists(dump_dir)

    font_file_path = dump_config.get_font_file_path()
    font = TTFont(font_file_path)
    image_font = ImageFont.truetype(font_file_path, dump_config.px)

    cmap = font.getBestCmap()
    units_per_em = font['head'].unitsPerEm
    hhea = font['hhea']
    metrics = font['hmtx'].metrics

    canvas_height = math.ceil(dump_config.px * (hhea.ascent - hhea.descent) / units_per_em)
    if canvas_height % 2 != 0:
        canvas_height += 1

    for code_point, glyph_name in cmap.items():
        unicode_block = configs.unidata_db.get_block_by_code_point(code_point)

        canvas_width = math.ceil(dump_config.px * metrics[glyph_name][0] / units_per_em)
        if canvas_width <= 0:
            canvas_width = dump_config.px
        elif canvas_width > dump_config.px and unicode_block.begin != 0xE000:  # Private Use Area
            canvas_width = dump_config.px

        uni_hex_name = f'{code_point:04X}'
        block_dir_name = f'{unicode_block.begin:04X}-{unicode_block.end:04X} {unicode_block.name}'
        glyph_file_to_dir = os.path.join(dump_dir, block_dir_name)
        if unicode_block.begin == 0x4E00:  # CJK Unified Ideographs
            glyph_file_to_dir = os.path.join(glyph_file_to_dir, f'{uni_hex_name[0:-2]}-')
        fs_util.make_dirs_if_not_exists(glyph_file_to_dir)
        glyph_file_to_path = os.path.join(glyph_file_to_dir, f'{uni_hex_name}.png')

        image = Image.new('RGBA', (canvas_width, canvas_height), (0, 0, 0, 0))
        ImageDraw.Draw(image).text(dump_config.offset_xy, chr(code_point), fill=(0, 0, 0), font=image_font)
        image.save(glyph_file_to_path)

        glyph_data = glyph_util.load_glyph_data_from_png(glyph_file_to_path)[0]
        glyph_util.save_glyph_data_to_png(glyph_data, glyph_file_to_path)

        logger.info(f'dump {glyph_file_to_path}')
