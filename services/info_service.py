import os

from PIL import ImageFont, Image, ImageDraw

import configs
from configs import workspace_define


def make_preview_image_file():
    px = configs.font_config[0]
    image_font = ImageFont.truetype(os.path.join(workspace_define.outputs_dir, f'fusion-pixel.otf'), px)
    image = Image.new('RGBA', (px * 35, px * 11), (255, 255, 255))
    ImageDraw.Draw(image).text((px, px), '缝合怪像素字体 / Fusion Pixel Font', fill=(0, 0, 0), font=image_font)
    ImageDraw.Draw(image).text((px, px * 3), '我们每天度过的称之为日常的生活，其实是一个个奇迹的连续也说不定。', fill=(0, 0, 0), font=image_font)
    ImageDraw.Draw(image).text((px, px * 5), 'THE QUICK BROWN FOX JUMPS OVER A LAZY DOG.', fill=(0, 0, 0), font=image_font)
    ImageDraw.Draw(image).text((px, px * 7), 'the quick brown fox jumps over a lazy dog.', fill=(0, 0, 0), font=image_font)
    ImageDraw.Draw(image).text((px, px * 9), '0123456789', fill=(0, 0, 0), font=image_font)
    image = image.resize((image.width * 2, image.height * 2), Image.NEAREST)
    image.save(os.path.join(workspace_define.outputs_dir, f'preview.png'))
