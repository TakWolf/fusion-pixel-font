import logging
import math
import os

import unidata_blocks
from PIL import ImageFont, Image, ImageDraw
from fontTools.ttLib import TTFont

from configs import DumpConfig
from utils import fs_util

logger = logging.getLogger('dump-service')


def dump_font(dump_config: DumpConfig):
    font = TTFont(dump_config.font_file_path)
    image_font = ImageFont.truetype(dump_config.font_file_path, dump_config.rasterize_size)

    canvas_height = math.ceil((font['hhea'].ascent - font['hhea'].descent) / font['head'].unitsPerEm * dump_config.rasterize_size)
    if (canvas_height - dump_config.font_size) % 2 != 0:
        canvas_height += 1

    for code_point, glyph_name in font.getBestCmap().items():
        block = unidata_blocks.get_block_by_code_point(code_point)

        canvas_width = math.ceil(font['hmtx'].metrics[glyph_name][0] / font['head'].unitsPerEm * dump_config.rasterize_size)
        if canvas_width <= 0:
            continue
        elif canvas_width > dump_config.font_size and block.code_start != 0xE000:  # Private Use Area
            canvas_width = dump_config.font_size

        image = Image.new('RGBA', (canvas_width, canvas_height), (0, 0, 0, 0))
        ImageDraw.Draw(image).text(dump_config.rasterize_offset, chr(code_point), fill=(0, 0, 0, 255), font=image_font)

        hex_name = f'{code_point:04X}'
        block_dir_name = f'{block.code_start:04X}-{block.code_end:04X} {block.name}'
        glyph_file_to_dir = os.path.join(dump_config.dump_dir, block_dir_name)
        if block.code_start == 0x4E00:  # CJK Unified Ideographs
            glyph_file_to_dir = os.path.join(glyph_file_to_dir, f'{hex_name[0:-2]}-')
        glyph_file_to_path = os.path.join(glyph_file_to_dir, f'{hex_name}.png')

        fs_util.make_dirs(glyph_file_to_dir)
        image.save(glyph_file_to_path)
        logger.info(f"Dump glyph: '{glyph_file_to_path}'")
