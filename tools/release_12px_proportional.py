import itertools

from tools import configs
from tools.configs import path_define, FontConfig, DumpConfig, FallbackConfig
from tools.services import update_service, dump_service, publish_service, info_service
from tools.services.font_service import DesignContext, FontContext


def main():
    font_size = 12
    width_mode = 'proportional'

    update_service.setup_ark_pixel_glyphs()

    for dump_config in DumpConfig.load_all()[font_size]:
        dump_service.dump_font(dump_config)

    for fallback_config in FallbackConfig.load_all()[font_size]:
        dump_service.apply_fallback(fallback_config)

    font_config = FontConfig.load(font_size)
    design_context = DesignContext.load(font_config, path_define.patch_glyphs_dir)
    design_context.standardized()
    design_context.fallback(DesignContext.load(font_config, path_define.ark_pixel_glyphs_dir))
    design_context.fallback(DesignContext.load(font_config, path_define.fallback_glyphs_dir))
    font_context = FontContext(design_context, width_mode)
    for font_format in itertools.chain(configs.font_formats, configs.font_collection_formats):
        font_context.make_fonts(font_format)
        publish_service.make_release_zip(font_size, width_mode, font_format)
    info_service.make_font_info(design_context, width_mode)
    info_service.make_alphabet_txt(design_context, width_mode)


if __name__ == '__main__':
    main()
