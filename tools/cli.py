import shutil
from typing import Literal

from cyclopts import App, Parameter
from loguru import logger
from pixel_font_knife import glyph_mapping_util

from tools import configs
from tools.configs import path_define, FontSize, WidthMode, FontFormat, Attachment
from tools.configs.dump import DumpConfig
from tools.configs.fallback import FallbackConfig
from tools.configs.font import FontConfig
from tools.services import update_service, dump_service, publish_service, info_service, template_service, image_service
from tools.services.font_service import DesignContext

app = App(
    version=configs.version,
    default_parameter=Parameter(consume_multiple=True),
)


@app.default
def main(
        cleanup: bool = False,
        font_sizes: set[FontSize] | None = None,
        width_modes: set[WidthMode] | None = None,
        font_formats: set[FontFormat] | None = None,
        attachments: set[Attachment | Literal['all']] | None = None,
):
    if font_sizes is None:
        font_sizes = configs.font_sizes
    else:
        font_sizes = sorted(font_sizes, key=lambda x: configs.font_sizes.index(x))
    if width_modes is None:
        width_modes = configs.width_modes
    else:
        width_modes = sorted(width_modes, key=lambda x: configs.width_modes.index(x))
    if font_formats is None:
        font_formats = configs.font_formats
    else:
        font_formats = sorted(font_formats, key=lambda x: configs.font_formats.index(x))
    if attachments is None:
        attachments = []
    elif 'all' in attachments:
        attachments = configs.attachments
    else:
        attachments = sorted(attachments, key=lambda x: configs.attachments.index(x))
    all_font_sizes = font_sizes == configs.font_sizes

    logger.info('cleanup = {}', cleanup)
    logger.info('font_sizes = {}', font_sizes)
    logger.info('width_modes = {}', width_modes)
    logger.info('font_formats = {}', font_formats)
    logger.info('attachments = {}', attachments)

    if cleanup and path_define.build_dir.exists():
        shutil.rmtree(path_define.build_dir)
        logger.info("Delete dir: '{}'", path_define.build_dir)

    update_service.setup_ark_pixel_glyphs()

    mappings = [glyph_mapping_util.load_mapping(mapping_file_path) for mapping_file_path in configs.mapping_file_paths]
    dump_configs = DumpConfig.load()
    fallback_configs = FallbackConfig.load()
    font_configs = {}
    design_contexts = {}
    for font_size in font_sizes:
        for dump_config in dump_configs[font_size]:
            dump_service.dump_font(dump_config)

        for fallback_config in fallback_configs[font_size]:
            dump_service.apply_fallback(fallback_config)

        font_config = FontConfig.load(font_size)
        font_configs[font_size] = font_config
        design_context = DesignContext.load(font_config, mappings)
        design_contexts[font_size] = design_context
        for width_mode in width_modes:
            for font_format in font_formats:
                design_context.make_fonts(width_mode, font_format)

    if 'release' in attachments:
        for font_size in font_sizes:
            for width_mode in width_modes:
                for font_format in font_formats:
                    publish_service.make_release_zip(font_size, width_mode, font_format)

    if 'info' in attachments:
        for font_size in font_sizes:
            design_context = design_contexts[font_size]
            for width_mode in width_modes:
                info_service.make_info(design_context, width_mode)

    if 'alphabet' in attachments:
        for font_size in font_sizes:
            design_context = design_contexts[font_size]
            for width_mode in width_modes:
                info_service.make_alphabet_txt(design_context, width_mode)

    if 'html' in attachments:
        for font_size in font_sizes:
            design_context = design_contexts[font_size]
            for width_mode in width_modes:
                template_service.make_alphabet_html(design_context, width_mode)
            template_service.make_demo_html(design_context)
        if all_font_sizes:
            template_service.make_index_html(font_configs)
            template_service.make_playground_html(font_configs)

    if 'image' in attachments:
        for font_size in font_sizes:
            font_config = font_configs[font_size]
            image_service.make_preview_image(font_config)


if __name__ == '__main__':
    app()
