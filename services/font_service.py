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

dot_em_units = 100


def collect_design_files(design_dirs):
    """
    收集可用字母表，生成设计文件映射表
    """
    alphabet = set()
    design_file_paths = {}
    for design_dir in reversed(design_dirs):
        if not os.path.isdir(design_dir):
            continue
        for design_file_parent_dir, _, design_file_names in os.walk(design_dir):
            for design_file_name in design_file_names:
                if not design_file_name.endswith('.png'):
                    continue
                design_file_path = os.path.join(design_file_parent_dir, design_file_name)
                uni_hex_name = design_file_name.replace('.png', '')
                if uni_hex_name == 'notdef':
                    design_file_paths['.notdef'] = design_file_path
                else:
                    code_point = int(uni_hex_name, 16)
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
    logger.info(f'draw glyph {design_file_path}')
    design_data, width, _ = glyph_util.load_design_data_from_png(design_file_path)
    outlines = glyph_util.get_outlines_from_design_data(design_data, dot_em_units)
    if is_ttf:
        pen = TTGlyphPen(None)
    else:
        pen = T2CharStringPen(width * dot_em_units, None)
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
    advance_width = width * dot_em_units
    if is_ttf:
        return pen.glyph(), advance_width
    else:
        return pen.getCharString(), advance_width


def _create_font_builder(name_strings, vertical_metrics, glyph_order, character_map, design_file_paths, is_ttf):
    units_per_em, ascent, descent, x_height, cap_height = vertical_metrics
    builder = FontBuilder(units_per_em, isTTF=is_ttf)
    builder.setupNameTable(name_strings)
    builder.setupGlyphOrder(glyph_order)
    builder.setupCharacterMap(character_map)
    glyphs = {}
    advance_widths = {}
    glyphs['.notdef'], advance_widths['.notdef'] = _draw_glyph(design_file_paths['.notdef'], ascent, is_ttf)
    for code_point, glyph_name in character_map.items():
        glyphs[glyph_name], advance_widths[glyph_name] = _draw_glyph(design_file_paths[code_point], ascent, is_ttf)
    if is_ttf:
        builder.setupGlyf(glyphs)
        horizontal_metrics = {glyph_name: (advance_width, glyphs[glyph_name].xMin) for glyph_name, advance_width in advance_widths.items()}
    else:
        builder.setupCFF(name_strings['psName'], {'FullName': name_strings['fullName']}, glyphs, {})
        horizontal_metrics = {glyph_name: (advance_width, glyphs[glyph_name].calcBounds(None)[0]) for glyph_name, advance_width in advance_widths.items()}
    builder.setupHorizontalMetrics(horizontal_metrics)
    builder.setupHorizontalHeader(ascent=ascent, descent=descent)
    builder.setupOS2(sTypoAscender=ascent, sTypoDescender=descent, usWinAscent=ascent, usWinDescent=-descent, sxHeight=x_height, sCapHeight=cap_height)
    builder.setupPost()
    return builder


def make_fonts(alphabet, design_file_paths):
    px, ascent_px, x_height_px, cap_height_px = configs.font_config
    descent_px = ascent_px - px
    units_per_em = px * dot_em_units
    ascent = ascent_px * dot_em_units
    descent = descent_px * dot_em_units
    x_height = x_height_px * dot_em_units
    cap_height = cap_height_px * dot_em_units
    vertical_metrics = units_per_em, ascent, descent, x_height, cap_height

    display_name = 'Fusion Pixel'
    unique_name = 'Fusion-Pixel'
    style_name = 'Regular'
    version = time.strftime('%Y.%m.%d')
    name_strings = {
        'copyright': 'Copyright (c) 2022, FusionPixel',
        'familyName': display_name,
        'styleName': style_name,
        'uniqueFontIdentifier': f'{unique_name}-{style_name};{version}',
        'fullName': display_name,
        'version': version,
        'psName': f'{unique_name}-{style_name}',
        'designer': 'FusionPixel',
        'description': 'Fusion pixel font.',
        'vendorURL': 'https://fusion-pixel-font.takwolf.com',
        'designerURL': 'https://fusion-pixel-font.takwolf.com',
        'licenseDescription': 'This Font Software is licensed under the SIL Open Font License, Version 1.1.',
        'licenseInfoURL': 'https://scripts.sil.org/OFL',
    }
    glyph_order = ['.notdef']
    character_map = {}
    for c in alphabet:
        code_point = ord(c)
        glyph_name = f'uni{code_point:04X}'
        glyph_order.append(glyph_name)
        character_map[code_point] = glyph_name
    otf_builder = _create_font_builder(name_strings, vertical_metrics, glyph_order, character_map, design_file_paths, False)
    otf_builder.save(os.path.join(workspace_define.outputs_dir, 'fusion-pixel.otf'))
    logger.info(f'make otf')
    otf_builder.font.flavor = 'woff2'
    otf_builder.save(os.path.join(workspace_define.outputs_dir, 'fusion-pixel.woff2'))
    logger.info(f'make woff2')
    ttf_builder = _create_font_builder(name_strings, vertical_metrics, glyph_order, character_map, design_file_paths, True)
    ttf_builder.save(os.path.join(workspace_define.outputs_dir, 'fusion-pixel.ttf'))
    logger.info(f'make ttf')
