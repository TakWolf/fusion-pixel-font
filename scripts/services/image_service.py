import logging
import os

from PIL import Image, ImageFont, ImageDraw
from PIL.ImageFont import FreeTypeFont

from scripts.configs import path_define, FontConfig
from scripts.utils import fs_util

logger = logging.getLogger('image-service')


def _load_font(font_config: FontConfig, width_mode: str, language_flavor: str, scale: int = 1) -> FreeTypeFont:
    file_path = os.path.join(path_define.outputs_dir, font_config.get_font_file_name(width_mode, language_flavor, 'woff2'))
    return ImageFont.truetype(file_path, font_config.size * scale)


def _draw_text(
        image: Image.Image,
        xy: tuple[float, float],
        text: str,
        font: FreeTypeFont,
        text_color: tuple[int, int, int, int] = (0, 0, 0, 255),
        shadow_color: tuple[int, int, int, int] = None,
        line_height: int = None,
        line_gap: int = 0,
        is_horizontal_centered: bool = False,
        is_vertical_centered: bool = False,
):
    draw = ImageDraw.Draw(image)
    x, y = xy
    default_line_height = sum(font.getmetrics())
    if line_height is None:
        line_height = default_line_height
    y += (line_height - default_line_height) / 2
    spacing = line_height + line_gap - font.getbbox('A')[3]
    if is_horizontal_centered:
        x -= draw.textbbox((0, 0), text, font=font)[2] / 2
    if is_vertical_centered:
        y -= line_height / 2
    if shadow_color is not None:
        draw.text((x + 1, y + 1), text, fill=shadow_color, font=font, spacing=spacing)
    draw.text((x, y), text, fill=text_color, font=font, spacing=spacing)


def make_preview_image_file(font_config: FontConfig):
    font_latin = _load_font(font_config, 'proportional', 'latin')
    font_zh_hans = _load_font(font_config, 'proportional', 'zh_hans')
    font_zh_hant = _load_font(font_config, 'proportional', 'zh_hant')
    font_ja = _load_font(font_config, 'proportional', 'ja')

    image = Image.new('RGBA', (font_config.size * 27, font_config.size * 2 + font_config.line_height * 9), (255, 255, 255, 255))
    _draw_text(image, (font_config.size, font_config.size), '缝合像素字体 / Fusion Pixel Font', font_zh_hans)
    _draw_text(image, (font_config.size, font_config.size + font_config.line_height), '我们度过的每个平凡的日常，也许就是连续发生的奇迹。', font_zh_hans)
    _draw_text(image, (font_config.size, font_config.size + font_config.line_height * 2), '我們度過的每個平凡的日常，也許就是連續發生的奇蹟。', font_zh_hant)
    _draw_text(image, (font_config.size, font_config.size + font_config.line_height * 3), '日々、私たちが過ごしている日常は、', font_ja)
    _draw_text(image, (font_config.size, font_config.size + font_config.line_height * 4), '実は奇跡の連続なのかもしれない。', font_ja)
    _draw_text(image, (font_config.size, font_config.size + font_config.line_height * 5), 'THE QUICK BROWN FOX JUMPS OVER A LAZY DOG.', font_latin)
    _draw_text(image, (font_config.size, font_config.size + font_config.line_height * 6), 'the quick brown fox jumps over a lazy dog.', font_latin)
    _draw_text(image, (font_config.size, font_config.size + font_config.line_height * 7), '0123456789', font_latin)
    _draw_text(image, (font_config.size, font_config.size + font_config.line_height * 8), '★☆☺☹♠♡♢♣♤♥♦♧☀☼♩♪♫♬☂☁⚓✈⚔☯', font_latin)
    image = image.resize((image.width * 2, image.height * 2), Image.Resampling.NEAREST)

    fs_util.make_dirs(path_define.outputs_dir)
    file_path = os.path.join(path_define.outputs_dir, font_config.preview_image_file_name)
    image.save(file_path)
    logger.info("Make preview image file: '%s'", file_path)
