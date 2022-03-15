import logging
import os
import time

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.ttGlyphPen import TTGlyphPen

import configs
from configs import workspace_define
from utils import glyph_util

logger = logging.getLogger('font-service')

em_dot_size = 100


def classify_design_files(design_dirs):
    """
    收集可用字母表，生成设计文件映射表
    """
    alphabet = set()
    design_file_paths = {}
    for design_dir in reversed(design_dirs):
        for design_file_parent_dir, _, design_file_names in os.walk(design_dir):
            for design_file_name in design_file_names:
                if design_file_name.endswith('.png'):
                    design_file_path = os.path.join(design_file_parent_dir, design_file_name)
                    uni_hex_name = design_file_name.replace('.png', '')
                    if uni_hex_name == 'notdef':
                        design_file_paths['.notdef'] = design_file_path
                    else:
                        code_point = int(uni_hex_name, 16)
                        if chr(code_point).isprintable():
                            design_file_paths[code_point] = design_file_path
                            alphabet.add(chr(code_point))
    alphabet = list(alphabet)
    alphabet.sort(key=lambda c: ord(c))
    return alphabet, design_file_paths


def _convert_point_to_open_type(point, ascent):
    """
    转换左上角坐标系为 OpenType 坐标系
    """
    x, y = point
    y = ascent - y
    return x, y


def _draw_glyph(design_file_path, ascent, is_ttf):
    logger.info(f'draw glyph by design file {design_file_path}')
    font_data, width, height = glyph_util.load_design_data_from_png(design_file_path)
    outlines = glyph_util.get_outlines_from_design_data(font_data, em_dot_size)
    if is_ttf:
        pen = TTGlyphPen(None)
    else:
        pen = T2CharStringPen(width * em_dot_size, None)
    if len(outlines) > 0:
        for outline_index, outline in enumerate(outlines):
            for point_index, point in enumerate(outline):
                point = _convert_point_to_open_type(point, ascent)
                if point_index == 0:
                    pen.moveTo(point)
                else:
                    pen.lineTo(point)
            if outline_index < len(outlines) - 1:
                pen.endPath()
            else:
                pen.closePath()
    else:
        pen.moveTo((0, 0))
        pen.closePath()
    advance_width = width * em_dot_size
    if is_ttf:
        return pen.glyph(), advance_width
    else:
        return pen.getCharString(), advance_width


def _create_font_builder(name_strings, units_per_em, ascent, descent, glyph_order, character_map, design_file_paths, is_ttf):
    builder = FontBuilder(units_per_em, isTTF=is_ttf)
    builder.setupGlyphOrder(glyph_order)
    builder.setupCharacterMap(character_map)
    glyphs = {}
    advance_widths = {}
    glyphs['.notdef'], advance_widths['.notdef'] = _draw_glyph(design_file_paths['.notdef'], ascent, is_ttf)
    for code_point, glyph_name in character_map.items():
        glyphs[glyph_name], advance_widths[glyph_name] = _draw_glyph(design_file_paths[code_point], ascent, is_ttf)
    if is_ttf:
        builder.setupGlyf(glyphs)
        metrics = {glyph_name: (advance_width, glyphs[glyph_name].xMin) for glyph_name, advance_width in advance_widths.items()}
    else:
        builder.setupCFF(name_strings['psName'], {'FullName': name_strings['fullName']}, glyphs, {})
        metrics = {glyph_name: (advance_width, glyphs[glyph_name].calcBounds(None)[0]) for glyph_name, advance_width in advance_widths.items()}
    builder.setupHorizontalMetrics(metrics)
    builder.setupHorizontalHeader(ascent=ascent, descent=descent)
    builder.setupNameTable(name_strings)
    builder.setupOS2(sTypoAscender=ascent, usWinAscent=ascent, usWinDescent=-descent)
    builder.setupPost()
    return builder


def make_fonts(alphabet, design_file_paths):
    px, ascent_px = configs.font_config
    descent_px = ascent_px - px
    units_per_em = px * em_dot_size
    ascent = ascent_px * em_dot_size
    descent = descent_px * em_dot_size

    display_name = f'Fusion Pixel {px}px'
    unique_name = f'Fusion-Pixel-{px}px'
    style_name = 'Regular'
    version = time.strftime('%Y%m%d')
    name_strings = {
        'familyName': display_name,
        'styleName': style_name,
        'uniqueFontIdentifier': f'{unique_name}-{style_name};{version}',
        'fullName': display_name,
        'version': version,
        'psName': f'{unique_name}-{style_name}',
        'description': 'Fusion pixel font.',
        'vendorURL': 'https://fusion-pixel-font.takwolf.com',
    }
    glyph_order = ['.notdef']
    character_map = {}
    for c in alphabet:
        code_point = ord(c)
        glyph_name = f'uni{code_point:04X}'
        glyph_order.append(glyph_name)
        character_map[code_point] = glyph_name
    otf_builder = _create_font_builder(name_strings, units_per_em, ascent, descent, glyph_order, character_map, design_file_paths, False)
    otf_builder.save(os.path.join(workspace_define.outputs_dir, 'fusion-pixel.otf'))
    logger.info(f'make {px}px otf')
    otf_builder.font.flavor = 'woff2'
    otf_builder.save(os.path.join(workspace_define.outputs_dir, 'fusion-pixel.woff2'))
    logger.info(f'make {px}px woff2')
    ttf_builder = _create_font_builder(name_strings, units_per_em, ascent, descent, glyph_order, character_map, design_file_paths, True)
    ttf_builder.save(os.path.join(workspace_define.outputs_dir, 'fusion-pixel.ttf'))
    logger.info(f'make {px}px ttf')
