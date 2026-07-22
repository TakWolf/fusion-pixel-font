import math

import unidata_blocks
from PIL import ImageFont, Image, ImageDraw
from fontTools.ttLib import TTFont
from loguru import logger
from pixel_font_knife.mono_bitmap import MonoBitmap

from tools import configs
from tools.configs import path_define, options
from tools.configs.options import FontSize


def dump_fonts(font_size: FontSize):
    for dump_config in configs.dump_configs[font_size]:
        dump_dir = path_define.dump_dir.joinpath(str(font_size), dump_config.dump_dir_name)
        logger.info("Dump glyphs: '{}'", dump_dir)

        font = TTFont(dump_config.font_file_path)
        image_font = ImageFont.truetype(dump_config.font_file_path, dump_config.rasterize_size)

        canvas_height = math.ceil((font['hhea'].ascent - font['hhea'].descent) / font['head'].unitsPerEm * dump_config.rasterize_size)
        if (canvas_height - font_size) % 2 != 0:
            canvas_height += 1

        for code_point, glyph_name in font.getBestCmap().items():
            c = chr(code_point)
            block = unidata_blocks.get_block_by_code_point(code_point)
            if not c.isprintable() and block.name != 'Private Use Area':
                continue

            canvas_width = math.ceil(font['hmtx'].metrics[glyph_name][0] / font['head'].unitsPerEm * dump_config.rasterize_size)
            if canvas_width <= 0:
                continue
            elif canvas_width > font_size and block.name != 'Private Use Area':
                canvas_width = font_size

            image = Image.new('RGBA', (canvas_width, canvas_height), (0, 0, 0, 0))
            ImageDraw.Draw(image).text(dump_config.rasterize_offset, c, fill=(0, 0, 0, 255), font=image_font)

            glyph_file_dir = dump_dir.joinpath(f'{block.code_start:04X}-{block.code_end:04X} {block.name}')
            code_name = f'{code_point:04X}'
            if block.name == 'CJK Unified Ideographs':
                glyph_file_dir = glyph_file_dir.joinpath(f'{code_name[0:-2]}-')
            glyph_file_path = glyph_file_dir.joinpath(f'{code_name}.png')
            glyph_file_dir.mkdir(parents=True, exist_ok=True)
            image.save(glyph_file_path)


def apply_fallbacks(font_size: FontSize):
    font_config = configs.font_configs[font_size]

    contexts = {}
    for fallback_config in configs.fallback_configs[font_size]:
        dir_from = path_define.dump_dir.joinpath(str(font_size), fallback_config.dir_from)
        assert dir_from.is_dir(), f"dump dir not exist: '{dir_from}'"
        logger.info("Fallback glyphs: '{}' '{}' '{}'", fallback_config.width_mode_dir_name, fallback_config.flavors, dir_from)

        if fallback_config.width_mode_dir_name in contexts:
            context = contexts[fallback_config.width_mode_dir_name]
        else:
            context = {}
            contexts[fallback_config.width_mode_dir_name] = context

        if fallback_config.width_mode_dir_name == 'proportional':
            canvas_size = font_config.canvas_size
        else:
            canvas_size = font_size

        for parent_dir, _, file_names in dir_from.walk():
            for file_name in file_names:
                if not file_name.endswith('.png'):
                    continue
                file_path = parent_dir.joinpath(file_name)

                bitmap = MonoBitmap.load_png(file_path)
                if bitmap.height > canvas_size:
                    padding = min((bitmap.height - canvas_size) // 2, bitmap.calculate_top_padding(), bitmap.calculate_bottom_padding())
                    if padding != 0:
                        bitmap = bitmap.resize(top=-padding, bottom=-padding)
                elif bitmap.height < canvas_size:
                    padding = (canvas_size - bitmap.height) // 2
                    bitmap = bitmap.resize(top=padding, bottom=padding)

                code_point = int(file_path.stem, 16)
                if code_point in context:
                    bitmap_strings = context[code_point]
                else:
                    bitmap_strings = {}
                    context[code_point] = bitmap_strings

                bitmap_string = str(bitmap)
                if bitmap_string in bitmap_strings:
                    _, flavors = bitmap_strings[bitmap_string]
                else:
                    flavors = set()
                    bitmap_strings[bitmap_string] = bitmap, flavors

                if fallback_config.flavors is not None:
                    flavors.update(fallback_config.flavors)

    for width_mode_dir_name, context in contexts.items():
        width_mode_dir = path_define.fallback_glyphs_dir.joinpath(str(font_size), width_mode_dir_name)
        for code_point, bitmap_strings in context.items():
            code_name = f'{code_point:04X}'
            block = unidata_blocks.get_block_by_code_point(code_point)
            file_dir = width_mode_dir.joinpath(f'{block.code_start:04X}-{block.code_end:04X} {block.name}')
            if block.name == 'CJK Unified Ideographs':
                file_dir = file_dir.joinpath(f'{code_name[0:-2]}-')
            file_dir.mkdir(parents=True, exist_ok=True)

            for bitmap, flavors in bitmap_strings.values():
                if len(flavors) > 0:
                    flavors = sorted(flavors, key=lambda x: options.language_file_flavors.index(x))
                    file_name = f'{code_name} {",".join(flavors)}.png'
                else:
                    file_name = f'{code_name}.png'

                file_path = file_dir.joinpath(file_name)
                bitmap.save_png(file_path)
        logger.info("Fallback context: {} '{}'", font_size, width_mode_dir_name)
