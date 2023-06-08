import json
import logging
import math
import os

import unidata_blocks
from PIL import ImageFont, Image, ImageDraw
from fontTools.ttLib import TTFont

import configs
from configs import path_define, DumpConfig
from utils import fs_util

logger = logging.getLogger('dump-service')


def _get_font_version(name: str) -> str:
    file_path = os.path.join(path_define.fonts_dir, name, 'version.json')
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.loads(file.read())['version']


def _dump_font(name: str, version: str, dump_config: DumpConfig):
    dump_dir = os.path.join(path_define.dump_dir, name, str(dump_config.font_size), dump_config.width_mode_dir_name)

    font_file_name = dump_config.font_file_name.format(version=version)
    font_file_path = os.path.join(path_define.fonts_dir, name, font_file_name)
    font = TTFont(font_file_path)
    image_font = ImageFont.truetype(font_file_path, dump_config.rasterize_font_size)

    canvas_height = math.ceil((font['hhea'].ascent - font['hhea'].descent) / font['head'].unitsPerEm * dump_config.rasterize_font_size)
    if (canvas_height - dump_config.font_size) % 2 != 0:
        canvas_height += 1

    for code_point, glyph_name in font.getBestCmap().items():
        block = unidata_blocks.get_block_by_code_point(code_point)

        canvas_width = math.ceil(font['hmtx'].metrics[glyph_name][0] / font['head'].unitsPerEm * dump_config.rasterize_font_size)
        if canvas_width <= 0:
            continue
        elif canvas_width > dump_config.font_size and block.code_start != 0xE000:  # Private Use Area
            canvas_width = dump_config.font_size

        image = Image.new('RGBA', (canvas_width, canvas_height), (0, 0, 0, 0))
        ImageDraw.Draw(image).text(dump_config.rasterize_offset, chr(code_point), fill=(0, 0, 0, 255), font=image_font)
        is_empty_glyph = True
        for y in range(canvas_height):
            for x in range(canvas_width):
                if image.getpixel((x, y))[3] > 127:
                    is_empty_glyph = False
                    break
        if is_empty_glyph:
            continue

        hex_name = f'{code_point:04X}'
        block_dir_name = f'{block.code_start:04X}-{block.code_end:04X} {block.name}'
        glyph_file_to_dir = os.path.join(dump_dir, block_dir_name)
        if block.code_start == 0x4E00:  # CJK Unified Ideographs
            glyph_file_to_dir = os.path.join(glyph_file_to_dir, f'{hex_name[0:-2]}-')
        glyph_file_to_path = os.path.join(glyph_file_to_dir, f'{hex_name}.png')

        fs_util.make_dirs(glyph_file_to_dir)
        image.save(glyph_file_to_path)
        logger.info(f"Dump glyph: '{glyph_file_to_path}'")


def _move_block_dir(from_name: str, from_width_mode: str, to_name: str, to_width_mode: str, font_size: int, block_name: str):
    block = unidata_blocks.get_block_by_name(block_name)
    block_dir_name = f'{block.code_start:04X}-{block.code_end:04X} {block.name}'
    from_dir = os.path.join(path_define.dump_dir, from_name, str(font_size), from_width_mode, block_dir_name)
    if os.path.exists(from_dir):
        to_width_mode_dir = os.path.join(path_define.dump_dir, to_name, str(font_size), to_width_mode)
        fs_util.make_dirs(to_width_mode_dir)
        to_dir = os.path.join(to_width_mode_dir, block_dir_name)
        os.rename(from_dir, to_dir)


def _discard_block_dir(name: str, width_mode: str, font_size: int, block_name: str):
    _move_block_dir(name, width_mode, f'{name}#discard', width_mode, font_size, block_name)


def _adjust_glyph_files():
    _move_block_dir('misaki', 'common', 'misaki#0', 'monospaced', 8, 'Basic Latin')

    _discard_block_dir('galmuri', 'monospaced', 10, 'Basic Latin')
    _discard_block_dir('galmuri', 'monospaced', 10, 'Latin Extended-A')
    _discard_block_dir('galmuri', 'monospaced', 10, 'Latin Extended-B')
    _discard_block_dir('galmuri', 'monospaced', 10, 'Greek and Coptic')
    _discard_block_dir('galmuri', 'monospaced', 10, 'Cyrillic')

    _discard_block_dir('galmuri', 'proportional', 10, 'Basic Latin')
    _discard_block_dir('galmuri', 'proportional', 10, 'Latin Extended-A')
    _discard_block_dir('galmuri', 'proportional', 10, 'Latin Extended-B')
    _discard_block_dir('galmuri', 'proportional', 10, 'Greek and Coptic')
    _discard_block_dir('galmuri', 'proportional', 10, 'Cyrillic')

    _discard_block_dir('zfull', 'common', 10, 'Basic Latin')
    _discard_block_dir('zfull', 'common', 10, 'Latin Extended-A')
    _discard_block_dir('zfull', 'common', 10, 'Latin Extended-B')
    _discard_block_dir('zfull', 'common', 10, 'Greek and Coptic')
    _discard_block_dir('zfull', 'common', 10, 'Cyrillic')
    _discard_block_dir('zfull', 'common', 10, 'Private Use Area')

    _discard_block_dir('cubic-11', 'common', 12, 'Basic Latin')
    _discard_block_dir('cubic-11', 'common', 12, 'Latin Extended-A')
    _discard_block_dir('cubic-11', 'common', 12, 'Latin Extended-B')
    _discard_block_dir('cubic-11', 'common', 12, 'Greek and Coptic')
    _discard_block_dir('cubic-11', 'common', 12, 'Cyrillic')
    _discard_block_dir('cubic-11', 'common', 12, 'Private Use Area')

    _discard_block_dir('galmuri', 'monospaced', 12, 'Basic Latin')
    _discard_block_dir('galmuri', 'monospaced', 12, 'Latin Extended-A')
    _discard_block_dir('galmuri', 'monospaced', 12, 'Latin Extended-B')
    _discard_block_dir('galmuri', 'monospaced', 12, 'Greek and Coptic')
    _discard_block_dir('galmuri', 'monospaced', 12, 'Cyrillic')

    _discard_block_dir('galmuri', 'proportional', 12, 'Basic Latin')
    _discard_block_dir('galmuri', 'proportional', 12, 'Latin Extended-A')
    _discard_block_dir('galmuri', 'proportional', 12, 'Latin Extended-B')
    _discard_block_dir('galmuri', 'proportional', 12, 'Greek and Coptic')
    _discard_block_dir('galmuri', 'proportional', 12, 'Cyrillic')


def dump_fonts():
    for name, dump_configs in configs.name_to_dump_configs.items():
        version = _get_font_version(name)
        for dump_config in dump_configs:
            _dump_font(name, version, dump_config)
    _adjust_glyph_files()
