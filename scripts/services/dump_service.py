import logging
import math
import os
import shutil

import unidata_blocks
from PIL import ImageFont, Image, ImageDraw
from fontTools.ttLib import TTFont

from scripts.configs.dump_config import DumpConfig
from scripts.configs.fallback_config import FallbackConfig
from scripts.utils import fs_util

logger = logging.getLogger('dump-service')


def dump_font(dump_config: DumpConfig, exclude_alphabet: set[str]):
    font = TTFont(dump_config.font_file_path)
    image_font = ImageFont.truetype(dump_config.font_file_path, dump_config.rasterize_size)

    canvas_height = math.ceil((font['hhea'].ascent - font['hhea'].descent) / font['head'].unitsPerEm * dump_config.rasterize_size)
    if (canvas_height - dump_config.font_size) % 2 != 0:
        canvas_height += 1

    for code_point, glyph_name in font.getBestCmap().items():
        c = chr(code_point)
        if c in exclude_alphabet:
            continue
        block = unidata_blocks.get_block_by_code_point(code_point)
        if not c.isprintable() and block.code_start != 0xE000:  # Private Use Area
            continue

        canvas_width = math.ceil(font['hmtx'].metrics[glyph_name][0] / font['head'].unitsPerEm * dump_config.rasterize_size)
        if canvas_width <= 0:
            continue
        elif canvas_width > dump_config.font_size and block.code_start != 0xE000:  # Private Use Area
            canvas_width = dump_config.font_size

        image = Image.new('RGBA', (canvas_width, canvas_height), (0, 0, 0, 0))
        ImageDraw.Draw(image).text(dump_config.rasterize_offset, chr(code_point), fill=(0, 0, 0, 255), font=image_font)

        block_dir_name = f'{block.code_start:04X}-{block.code_end:04X} {block.name}'
        glyph_file_to_dir = os.path.join(dump_config.dump_dir, block_dir_name)
        hex_name = f'{code_point:04X}'
        if block.code_start == 0x4E00:  # CJK Unified Ideographs
            glyph_file_to_dir = os.path.join(glyph_file_to_dir, f'{hex_name[0:-2]}-')
        glyph_file_to_path = os.path.join(glyph_file_to_dir, f'{hex_name}.png')

        fs_util.make_dirs(glyph_file_to_dir)
        image.save(glyph_file_to_path)
        logger.info("Dump glyph: '%s'", glyph_file_to_path)


def apply_fallback(fallback_config: FallbackConfig):
    assert os.path.isdir(fallback_config.from_dir), f"Dump dir not exist: '{fallback_config.from_dir}'"
    for glyph_file_from_dir, _, glyph_file_names in os.walk(fallback_config.from_dir):
        for glyph_file_name in glyph_file_names:
            if not glyph_file_name.endswith('.png'):
                continue
            glyph_file_from_path = os.path.join(glyph_file_from_dir, glyph_file_name)
            hex_name = glyph_file_name.removesuffix('.png')
            code_point = int(hex_name, 16)
            block = unidata_blocks.get_block_by_code_point(code_point)
            block_dir_name = f'{block.code_start:04X}-{block.code_end:04X} {block.name}'
            glyph_file_to_dir = os.path.join(fallback_config.to_dir, block_dir_name)
            if block.code_start == 0x4E00:  # CJK Unified Ideographs
                glyph_file_to_dir = os.path.join(glyph_file_to_dir, f'{hex_name[0:-2]}-')
            if fallback_config.flavor is not None:
                glyph_file_name = f'{hex_name} {fallback_config.flavor}.png'
            glyph_file_to_path = os.path.join(glyph_file_to_dir, glyph_file_name)
            fs_util.make_dirs(glyph_file_to_dir)
            shutil.copyfile(glyph_file_from_path, glyph_file_to_path)
            logger.info("Copy glyph file: '%s'", glyph_file_to_path)
