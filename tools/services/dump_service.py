import math
import shutil

import unidata_blocks
from PIL import ImageFont, Image, ImageDraw
from fontTools.ttLib import TTFont
from loguru import logger

from tools.configs.dump import DumpConfig
from tools.configs.fallback import FallbackConfig


def dump_font(dump_config: DumpConfig):
    logger.info("Dump glyphs: '{}'", dump_config.dump_dir)
    font = TTFont(dump_config.font_file_path)
    image_font = ImageFont.truetype(dump_config.font_file_path, dump_config.rasterize_size)

    canvas_height = math.ceil((font['hhea'].ascent - font['hhea'].descent) / font['head'].unitsPerEm * dump_config.rasterize_size)
    if (canvas_height - dump_config.font_size) % 2 != 0:
        canvas_height += 1

    for code_point, glyph_name in font.getBestCmap().items():
        c = chr(code_point)
        block = unidata_blocks.get_block_by_code_point(code_point)
        if not c.isprintable() and block.name != 'Private Use Area':
            continue

        canvas_width = math.ceil(font['hmtx'].metrics[glyph_name][0] / font['head'].unitsPerEm * dump_config.rasterize_size)
        if canvas_width <= 0:
            continue
        elif canvas_width > dump_config.font_size and block.name != 'Private Use Area':
            canvas_width = dump_config.font_size

        image = Image.new('RGBA', (canvas_width, canvas_height), (0, 0, 0, 0))
        ImageDraw.Draw(image).text(dump_config.rasterize_offset, c, fill=(0, 0, 0, 255), font=image_font)

        glyph_file_dir = dump_config.dump_dir.joinpath(f'{block.code_start:04X}-{block.code_end:04X} {block.name}')
        code_name = f'{code_point:04X}'
        if block.name == 'CJK Unified Ideographs':
            glyph_file_dir = glyph_file_dir.joinpath(f'{code_name[0:-2]}-')
        glyph_file_path = glyph_file_dir.joinpath(f'{code_name}.png')
        glyph_file_dir.mkdir(parents=True, exist_ok=True)
        image.save(glyph_file_path)


def apply_fallback(fallback_config: FallbackConfig):
    assert fallback_config.dir_from.is_dir(), f"dump dir not exist: '{fallback_config.dir_from}'"
    logger.info("Fallback glyphs: '{}' '{}' -> '{}'", fallback_config.flavor, fallback_config.dir_from, fallback_config.dir_to)
    for glyph_file_dir_from, _, glyph_file_names in fallback_config.dir_from.walk():
        for glyph_file_name in glyph_file_names:
            if not glyph_file_name.endswith('.png'):
                continue
            glyph_file_path_from = glyph_file_dir_from.joinpath(glyph_file_name)
            code_name = glyph_file_path_from.stem
            code_point = int(code_name, 16)
            block = unidata_blocks.get_block_by_code_point(code_point)
            glyph_file_dir_to = fallback_config.dir_to.joinpath(f'{block.code_start:04X}-{block.code_end:04X} {block.name}')
            if block.name == 'CJK Unified Ideographs':
                glyph_file_dir_to = glyph_file_dir_to.joinpath(f'{code_name[0:-2]}-')
            if fallback_config.flavor is not None:
                glyph_file_name = f'{code_name} {fallback_config.flavor}.png'
            glyph_file_path_to = glyph_file_dir_to.joinpath(glyph_file_name)
            glyph_file_dir_to.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(glyph_file_path_from, glyph_file_path_to)
