import logging
import os
import shutil
import unicodedata

import png
import unidata_blocks
from pixel_font_builder import FontBuilder, Glyph, StyleName, SerifMode

import configs
from configs import FontConfig, path_define
from utils import fs_util

logger = logging.getLogger('font-service')


def _load_glyph_data_from_png(file_path: str) -> tuple[list[list[int]], int, int]:
    width, height, bitmap, _ = png.Reader(filename=file_path).read()
    data = []
    for bitmap_row in bitmap:
        data_row = []
        for x in range(0, width * 4, 4):
            alpha = bitmap_row[x + 3]
            if alpha > 127:
                data_row.append(1)
            else:
                data_row.append(0)
        data.append(data_row)
    return data, width, height


def _save_glyph_data_to_png(data: list[list[int]], file_path: str):
    bitmap = []
    for data_row in data:
        bitmap_row = []
        for x in data_row:
            bitmap_row.append(0)
            bitmap_row.append(0)
            bitmap_row.append(0)
            if x == 0:
                bitmap_row.append(0)
            else:
                bitmap_row.append(255)
        bitmap.append(bitmap_row)
    png.from_array(bitmap, 'RGBA').save(file_path)


def format_glyph_files(font_config: FontConfig):
    root_dir = os.path.join(path_define.glyphs_dir, str(font_config.size))
    tmp_dir = os.path.join(path_define.glyphs_tmp_dir, str(font_config.size))
    fs_util.delete_dir(tmp_dir)
    for width_mode_dir_name in configs.width_mode_dir_names:
        width_mode_dir = os.path.join(root_dir, width_mode_dir_name)
        if not os.path.isdir(width_mode_dir):
            continue
        width_mode_tmp_dir = os.path.join(tmp_dir, width_mode_dir_name)
        for glyph_file_from_dir, glyph_file_name in fs_util.walk_files(width_mode_dir):
            if not glyph_file_name.endswith('.png'):
                continue
            glyph_file_from_path = os.path.join(glyph_file_from_dir, glyph_file_name)
            if glyph_file_name == 'notdef.png':
                east_asian_width = 'F'
                block = None
                glyph_file_to_dir = width_mode_tmp_dir
            else:
                hex_name = glyph_file_name.removesuffix('.png')
                code_point = int(hex_name, 16)
                c = chr(code_point)
                east_asian_width = unicodedata.east_asian_width(c)
                block = unidata_blocks.get_block_by_code_point(code_point)
                block_dir_name = f'{block.code_start:04X}-{block.code_end:04X} {block.name}'
                glyph_file_to_dir = os.path.join(width_mode_tmp_dir, block_dir_name)
                if block.code_start == 0x4E00:  # CJK Unified Ideographs
                    glyph_file_to_dir = os.path.join(glyph_file_to_dir, f'{hex_name[0:-2]}-')
            glyph_file_to_path = os.path.join(glyph_file_to_dir, glyph_file_name)
            assert not os.path.exists(glyph_file_to_path), f"Glyph file already exists: '{glyph_file_to_path}'"

            glyph_data, glyph_width, glyph_height = _load_glyph_data_from_png(glyph_file_from_path)

            if width_mode_dir_name == 'common' or width_mode_dir_name == 'monospaced':
                assert glyph_height == font_config.size, f"Incorrect glyph data: '{glyph_file_from_path}'"

                # H/Halfwidth or Na/Narrow
                if east_asian_width == 'H' or east_asian_width == 'Na':
                    assert glyph_width == font_config.size / 2, f"Incorrect glyph data: '{glyph_file_from_path}'"
                # F/Fullwidth or W/Wide
                elif east_asian_width == 'F' or east_asian_width == 'W':
                    assert glyph_width == font_config.size, f"Incorrect glyph data: '{glyph_file_from_path}'"
                # A/Ambiguous or N/Neutral
                else:
                    assert glyph_width == font_config.size / 2 or glyph_width == font_config.size, f"Incorrect glyph data: '{glyph_file_from_path}'"

                if block is not None:
                    if block.code_start == 0x4E00:  # CJK Unified Ideographs
                        if any(alpha != 0 for alpha in glyph_data[0]):
                            raise AssertionError(f"Incorrect glyph data: '{glyph_file_from_path}'")
                        if any(glyph_data[i][-1] != 0 for i in range(0, len(glyph_data))):
                            raise AssertionError(f"Incorrect glyph data: '{glyph_file_from_path}'")

            if width_mode_dir_name == 'proportional':
                assert glyph_height >= font_config.size, f"Incorrect glyph data: '{glyph_file_from_path}'"
                assert (glyph_height - font_config.size) % 2 == 0, f"Incorrect glyph data: '{glyph_file_from_path}'"

                if glyph_height > font_config.line_height:
                    for i in range(int((glyph_height - font_config.line_height) / 2)):
                        glyph_data.pop(0)
                        glyph_data.pop()
                elif glyph_height < font_config.line_height:
                    for i in range(int((font_config.line_height - glyph_height) / 2)):
                        glyph_data.insert(0, [0 for _ in range(glyph_width)])
                        glyph_data.append([0 for _ in range(glyph_width)])

            fs_util.make_dirs(glyph_file_to_dir)
            _save_glyph_data_to_png(glyph_data, glyph_file_to_path)
            logger.info(f"Format glyph file: '{glyph_file_to_path}'")
        width_mode_old_dir = os.path.join(tmp_dir, f'{width_mode_dir_name}.old')
        os.rename(width_mode_dir, width_mode_old_dir)
        os.rename(width_mode_tmp_dir, width_mode_dir)
        shutil.rmtree(width_mode_old_dir)


class DesignContext:
    def __init__(
            self,
            alphabet_group: dict[str, list[str]],
            fallback_count_infos_group: dict[str, dict[str, int]],
            character_mapping_group: dict[str, dict[int, str]],
            glyph_file_paths_group: dict[str, dict[str, str]],
    ):
        self._alphabet_group = alphabet_group
        self._fallback_count_infos_group = fallback_count_infos_group
        self._character_mapping_group = character_mapping_group
        self._glyph_file_paths_group = glyph_file_paths_group
        self._glyph_data_pool = dict[str, tuple[list[list[int]], int, int]]()

    def get_alphabet(self, width_mode: str) -> list[str]:
        return self._alphabet_group[width_mode]

    def get_fallback_count_infos(self, width_mode: str) -> dict[str, int]:
        return self._fallback_count_infos_group[width_mode]

    def get_character_mapping(self, width_mode: str) -> dict[int, str]:
        return self._character_mapping_group[width_mode]

    def get_glyph_file_paths(self, width_mode: str) -> dict[str, str]:
        return self._glyph_file_paths_group[width_mode]

    def load_glyph_data(self, glyph_file_path: str) -> tuple[list[list[int]], int, int]:
        if glyph_file_path in self._glyph_data_pool:
            glyph_data, glyph_width, glyph_height = self._glyph_data_pool[glyph_file_path]
        else:
            glyph_data, glyph_width, glyph_height = _load_glyph_data_from_png(glyph_file_path)
            self._glyph_data_pool[glyph_file_path] = glyph_data, glyph_width, glyph_height
        return glyph_data, glyph_width, glyph_height


def collect_glyph_files(font_config: FontConfig) -> DesignContext:
    character_mapping_group = {}
    glyph_file_paths_group = {}
    for width_mode in configs.width_modes:
        character_mapping_group[width_mode] = dict[int, str]()
        glyph_file_paths_group[width_mode] = dict[str, str]()

    glyphs_dir_infos = [('base', os.path.join(path_define.glyphs_dir, str(font_config.size)))]
    for name in configs.font_size_to_fallback_names[font_config.size]:
        glyphs_dir_infos.append((name, os.path.join(path_define.dump_dir, name, str(font_config.size))))
    for name, glyphs_dir in reversed(glyphs_dir_infos):
        glyph_file_paths_cellar = {}
        for width_mode_dir_name in configs.width_mode_dir_names:
            glyph_file_paths_cellar[width_mode_dir_name] = dict[str, str]()
            width_mode_dir = os.path.join(glyphs_dir, width_mode_dir_name)
            if not os.path.isdir(width_mode_dir):
                continue
            for glyph_file_dir, glyph_file_name in fs_util.walk_files(width_mode_dir):
                if not glyph_file_name.endswith('.png'):
                    continue
                glyph_file_path = os.path.join(glyph_file_dir, glyph_file_name)
                if glyph_file_name == 'notdef.png':
                    glyph_file_paths_cellar[width_mode_dir_name]['.notdef'] = glyph_file_path
                else:
                    hex_name = glyph_file_name.removesuffix('.png')
                    code_point = int(hex_name, 16)
                    glyph_name = f'uni{code_point:04X}'
                    if width_mode_dir_name == 'common' or width_mode_dir_name == 'monospaced':
                        character_mapping_group['monospaced'][code_point] = glyph_name
                    if width_mode_dir_name == 'common' or width_mode_dir_name == 'proportional':
                        character_mapping_group['proportional'][code_point] = glyph_name
                    assert glyph_name not in glyph_file_paths_cellar[width_mode_dir_name], f"Glyph name '{glyph_name}' already exists"
                    glyph_file_paths_cellar[width_mode_dir_name][glyph_name] = glyph_file_path
        for width_mode in configs.width_modes:
            glyph_file_paths_group[width_mode].update(glyph_file_paths_cellar['common'])
            glyph_file_paths_group[width_mode].update(glyph_file_paths_cellar[width_mode])

    alphabet_group = {}
    fallback_count_infos_group = {}
    for width_mode in configs.width_modes:
        character_mapping = character_mapping_group[width_mode]
        alphabet = [chr(code_point) for code_point in character_mapping]
        alphabet.sort()
        alphabet_group[width_mode] = alphabet

        glyph_file_paths = glyph_file_paths_group[width_mode]
        fallback_count_infos = dict[str, int]()
        for name, glyphs_dir in glyphs_dir_infos:
            name = name.split('#')[0]
            count = fallback_count_infos.get(name, 0)
            for glyph_file_path in glyph_file_paths.values():
                if glyph_file_path.startswith(glyphs_dir):
                    count += 1
            fallback_count_infos[name] = count
        fallback_count_infos_group[width_mode] = dict[str, int]()
        for name, count in fallback_count_infos.items():
            if count > 0:
                fallback_count_infos_group[width_mode][name] = count

    return DesignContext(alphabet_group, fallback_count_infos_group, character_mapping_group, glyph_file_paths_group)


def _create_builder(font_config: FontConfig, context: DesignContext, width_mode: str) -> FontBuilder:
    font_attrs = font_config.get_attrs(width_mode)
    builder = FontBuilder(
        font_config.size,
        font_attrs.ascent,
        font_attrs.descent,
        font_attrs.x_height,
        font_attrs.cap_height,
    )

    builder.character_mapping.update(context.get_character_mapping(width_mode))
    for glyph_name, glyph_file_path in context.get_glyph_file_paths(width_mode).items():
        glyph_data, glyph_width, glyph_height = context.load_glyph_data(glyph_file_path)
        offset_y = font_attrs.box_origin_y + int((glyph_height - font_config.size) / 2) - glyph_height
        builder.add_glyph(Glyph(
            name=glyph_name,
            advance_width=glyph_width,
            offset=(0, offset_y),
            data=glyph_data,
        ))

    builder.meta_infos.version = configs.version
    builder.meta_infos.family_name = f'{FontConfig.FAMILY_NAME} {font_config.size}px {width_mode.capitalize()}'
    builder.meta_infos.style_name = StyleName.REGULAR
    builder.meta_infos.serif_mode = SerifMode.SANS_SERIF
    builder.meta_infos.width_mode = width_mode.capitalize()
    builder.meta_infos.manufacturer = FontConfig.MANUFACTURER
    builder.meta_infos.designer = FontConfig.DESIGNER
    builder.meta_infos.description = FontConfig.DESCRIPTION
    builder.meta_infos.copyright_info = FontConfig.COPYRIGHT_INFO
    builder.meta_infos.license_info = FontConfig.LICENSE_INFO
    builder.meta_infos.vendor_url = FontConfig.VENDOR_URL
    builder.meta_infos.designer_url = FontConfig.DESIGNER_URL
    builder.meta_infos.license_url = FontConfig.LICENSE_URL

    return builder


def make_font_files(font_config: FontConfig, context: DesignContext, width_mode: str):
    fs_util.make_dirs(path_define.outputs_dir)

    builder = _create_builder(font_config, context, width_mode)
    otf_builder = builder.to_otf_builder()
    otf_file_path = os.path.join(path_define.outputs_dir, font_config.get_font_file_name(width_mode, 'otf'))
    otf_builder.save(otf_file_path)
    logger.info(f"Make font file: '{otf_file_path}'")
    otf_builder.font.flavor = 'woff2'
    woff2_file_path = os.path.join(path_define.outputs_dir, font_config.get_font_file_name(width_mode, 'woff2'))
    otf_builder.save(woff2_file_path)
    logger.info(f"Make font file: '{woff2_file_path}'")
    ttf_file_path = os.path.join(path_define.outputs_dir, font_config.get_font_file_name(width_mode, 'ttf'))
    builder.save_ttf(ttf_file_path)
    logger.info(f"Make font file: '{ttf_file_path}'")
    bdf_file_path = os.path.join(path_define.outputs_dir, font_config.get_font_file_name(width_mode, 'bdf'))
    builder.save_bdf(bdf_file_path)
    logger.info(f"Make font file: '{bdf_file_path}'")
