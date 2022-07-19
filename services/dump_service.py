import logging
import math
import os

from PIL import ImageFont, Image, ImageDraw
from fontTools.ttLib import TTFont

import configs
from configs import workspace_define

logger = logging.getLogger('dump-service')


def dump_font(dump_config):
    outputs_dir = os.path.join(workspace_define.dump_dir, dump_config.name)
    font = TTFont(dump_config.font_path)
    cmap = font.getBestCmap()
    units_per_em = font['head'].unitsPerEm
    metrics = font['hmtx'].metrics
    image_font = ImageFont.truetype(dump_config.font_path, dump_config.px)
    for code_point, glyph_name in cmap.items():
        unicode_block = configs.unidata_db.get_block_by_code_point(code_point)
        canvas_width = math.ceil(metrics[glyph_name][0] / units_per_em * configs.target_px)
        if canvas_width <= 0:
            canvas_width = configs.target_px
        elif canvas_width > configs.target_px and unicode_block.name != 'Private Use Area':
            canvas_width = configs.target_px
        block_dir_name = f'{unicode_block.begin:04X}-{unicode_block.end:04X} {unicode_block.name}'
        output_png_file_to_dir = os.path.join(outputs_dir, block_dir_name)
        uni_hex_name = f'{code_point:04X}'
        if unicode_block.name == 'CJK Unified Ideographs':
            output_png_file_to_dir = os.path.join(output_png_file_to_dir, f'{uni_hex_name[0:-2]}-')
        if not os.path.exists(output_png_file_to_dir):
            os.makedirs(output_png_file_to_dir)
        image = Image.new('RGBA', (canvas_width, configs.target_px), (0, 0, 0, 0))
        ImageDraw.Draw(image).text(dump_config.offset_xy, chr(code_point), fill=(0, 0, 0), font=image_font)
        output_png_path = os.path.join(output_png_file_to_dir, f'{code_point:04X}.png')
        image.save(output_png_path)
        logger.info(f'make {output_png_path}')
    return outputs_dir
