import logging
import math
import os.path

from PIL import ImageFont, Image, ImageDraw
from fontTools.ttLib import TTFont

import configs
from configs import workspace_define

logger = logging.getLogger('dump-service')


def dump_font(dump_config):
    outputs_dir = os.path.join(workspace_define.dump_outputs_dir, dump_config.name)
    if not os.path.exists(outputs_dir):
        os.makedirs(outputs_dir)
    font = TTFont(dump_config.font_path)
    cmap = font.getBestCmap()
    units_per_em = font['head'].unitsPerEm
    metrics = font['hmtx'].metrics
    image_font = ImageFont.truetype(dump_config.font_path, dump_config.px)
    for code_point, glyph_name in cmap.items():
        canvas_width = math.ceil(metrics[glyph_name][0] / units_per_em * configs.target_px)
        if canvas_width <= 0 or canvas_width > configs.target_px:
            canvas_width = configs.target_px
        image = Image.new('RGBA', (canvas_width, configs.target_px), (0, 0, 0, 0))
        ImageDraw.Draw(image).text(dump_config.offset_xy, chr(code_point), fill=(0, 0, 0), font=image_font)
        output_png_path = os.path.join(outputs_dir, f'{code_point:04X}.png')
        image.save(output_png_path)
        logger.info(f'make: {output_png_path}')
    return outputs_dir
