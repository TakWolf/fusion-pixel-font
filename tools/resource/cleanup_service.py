from loguru import logger
from pixel_font_knife.cmap.context import CmapContext

from tools.config import path_define, options
from tools.config.options import FontSize


def cleanup_cmap_glyphs(font_size: FontSize) -> None:
    ark_contexts = {
        glyph_scope: CmapContext.load(
            path_define.ARK_PIXEL_GLYPHS_DIR.joinpath(str(font_size), 'cmap', glyph_scope),
            allowed_flavors=options.LANGUAGE_FLAVORS,
        )
        for glyph_scope in options.GLYPH_SCOPES
    }
    patch_contexts = {
        glyph_scope: CmapContext.load(
            path_define.PATCH_GLYPHS_DIR.joinpath(str(font_size), 'cmap', glyph_scope),
            allowed_flavors=options.LANGUAGE_FLAVORS,
        )
        for glyph_scope in options.GLYPH_SCOPES
    }

    pending_deletion = set()

    for code_point, glyph_variants in patch_contexts['common'].items():
        if code_point in ark_contexts['common'] or (code_point in ark_contexts['monospaced'] and code_point in ark_contexts['proportional']):
            pending_deletion.update(glyph_variants.values())

    for code_point, glyph_variants in patch_contexts['monospaced'].items():
        if code_point in ark_contexts['common'] or code_point in ark_contexts['monospaced']:
            pending_deletion.update(glyph_variants.values())

    for code_point, glyph_variants in patch_contexts['proportional'].items():
        if code_point in ark_contexts['common'] or code_point in ark_contexts['proportional']:
            pending_deletion.update(glyph_variants.values())

    for glyph_file in pending_deletion:
        glyph_file.file_path.unlink()
        logger.info('Delete: {!r}', str(glyph_file.file_path))
