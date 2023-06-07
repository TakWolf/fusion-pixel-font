import logging
import math
import os

from PIL import Image, ImageFont, ImageDraw

from configs import path_define, font_config
from utils import fs_util

logger = logging.getLogger('image-service')


def _load_font(width_mode, px_scale=1):
    font_file_path = os.path.join(path_define.outputs_dir, font_config.get_font_file_name(width_mode, 'woff2'))
    return ImageFont.truetype(font_file_path, font_config.px * px_scale)


def _draw_text(image, xy, text, font, text_color=(0, 0, 0), shadow_color=None, line_height=None, line_gap=0, is_horizontal_centered=False, is_vertical_centered=False):
    draw = ImageDraw.Draw(image)
    x, y = xy
    default_line_height = sum(font.getmetrics())
    if line_height is None:
        line_height = default_line_height
    y += (line_height - default_line_height) / 2
    spacing = line_height + line_gap - font.getsize('A')[1]
    if is_horizontal_centered:
        x -= draw.textbbox((0, 0), text, font=font)[2] / 2
    if is_vertical_centered:
        y -= line_height / 2
    if shadow_color is not None:
        draw.text((x + 1, y + 1), text, fill=shadow_color, font=font, spacing=spacing)
    draw.text((x, y), text, fill=text_color, font=font, spacing=spacing)


def make_preview_image_file():
    font = _load_font('proportional')
    lines = [
        '缝合怪像素字体 / Fusion Pixel Font',
        '我们每天度过的称之为日常的生活，其实是一个个奇迹的连续也说不定。',
        '我們每天度過的稱之為日常的生活，其實是一個個奇跡的連續也說不定。',
        '日々、私たちが過ごしている日常は、実は奇跡の連続なのかもしれない。',
        'THE QUICK BROWN FOX JUMPS OVER A LAZY DOG.',
        'the quick brown fox jumps over a lazy dog.',
        '0123456789',
        '★☆☺☹♠♡♢♣♤♥♦♧☀☼♩♪♫♬☂☁⚓✈⚔☯',
        '☜☝☞☟♔♕♖♗♘♙♚♛♜♝♞♟',
    ]
    content_width = 0
    for line in lines:
        line_width = math.ceil(font.getlength(line))
        if line_width > content_width:
            content_width = line_width
    content_height = font_config.display_line_height_px * len(lines)

    image_width = font_config.px * 2 + content_width
    image_height = font_config.px * 2 + content_height
    image = Image.new('RGBA', (image_width, image_height), (255, 255, 255))
    cursor_x = font_config.px
    cursor_y = font_config.px
    for line in lines:
        _draw_text(image, (cursor_x, cursor_y), line, font)
        cursor_y += font_config.display_line_height_px
    image = image.resize((image.width * 2, image.height * 2), Image.NEAREST)

    fs_util.make_dirs(path_define.outputs_dir)
    image_file_path = os.path.join(path_define.outputs_dir, 'preview.png')
    image.save(image_file_path)
    logger.info(f'make {image_file_path}')
