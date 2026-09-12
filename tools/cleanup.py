import itertools
import shutil

from loguru import logger
from pixel_font_knife import glyph_file_util, glyph_mapping_util, fs_util

from tools import configs
from tools.configs import path_define, options
from tools.services import setup_service


def main() -> None:
    setup_service.setup_ark_pixel()

    for font_size in options.FONT_SIZES:
        ark_contexts = {}
        patch_contexts = {}
        for width_mode_dir_name in itertools.chain(['common'], options.WIDTH_MODES):
            ark_context = glyph_file_util.load_context(path_define.ARK_PIXEL_GLYPHS_DIR.joinpath(str(font_size), width_mode_dir_name))
            for mapping in configs.MAPPINGS:
                glyph_mapping_util.apply_mapping(ark_context, mapping)
            ark_contexts[width_mode_dir_name] = ark_context

            patch_context = glyph_file_util.load_context(path_define.PATCH_GLYPHS_DIR.joinpath(str(font_size), width_mode_dir_name))
            patch_contexts[width_mode_dir_name] = patch_context

        pending_deletion = set()

        for code_point, flavor_group in patch_contexts['common'].items():
            if code_point in ark_contexts['common'] or (code_point in ark_contexts['monospaced'] and code_point in ark_contexts['proportional']):
                pending_deletion.update(flavor_group.values())

        for code_point, flavor_group in patch_contexts['monospaced'].items():
            if code_point in ark_contexts['common'] or code_point in ark_contexts['monospaced']:
                pending_deletion.update(flavor_group.values())

        for code_point, flavor_group in patch_contexts['proportional'].items():
            if code_point in ark_contexts['common'] or code_point in ark_contexts['proportional']:
                pending_deletion.update(flavor_group.values())

        for glyph_file in pending_deletion:
            glyph_file.file_path.unlink()
            logger.info("Delete: '{}'", glyph_file.file_path)

    for file_dir, _, _ in path_define.PATCH_GLYPHS_DIR.walk(top_down=False):
        if fs_util.is_empty_dir(file_dir):
            shutil.rmtree(file_dir)


if __name__ == '__main__':
    main()
