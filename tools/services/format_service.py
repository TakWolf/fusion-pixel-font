import itertools

from pixel_font_knife import glyph_file_util

from tools import configs
from tools.configs import path_define
from tools.configs.font import FontConfig


def format_glyphs(font_config: FontConfig):
    for width_mode_dir_name in itertools.chain(['common'], configs.width_modes):
        width_mode_dir = path_define.patch_glyphs_dir.joinpath(str(font_config.font_size), width_mode_dir_name)
        context = glyph_file_util.load_context(width_mode_dir)
        glyph_file_util.normalize_context(context, width_mode_dir, configs.language_file_flavors)
