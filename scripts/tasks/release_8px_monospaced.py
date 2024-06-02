from scripts.configs import path_define, FontConfig, DumpConfig, FallbackConfig
from scripts.services import update_service, dump_service, publish_service, info_service
from scripts.services.font_service import DesignContext, FontContext


def main():
    font_size = 8
    width_mode = 'monospaced'

    update_service.setup_ark_pixel_glyphs()

    for dump_config in DumpConfig.load_all()[font_size]:
        dump_service.dump_font(dump_config)

    for fallback_config in FallbackConfig.load_all()[font_size]:
        dump_service.apply_fallback(fallback_config)

    font_config = FontConfig.load(font_size)
    design_context = DesignContext.load(font_config, path_define.patch_glyphs_dir)
    design_context.standardize()
    design_context.fallback(DesignContext.load(font_config, path_define.ark_pixel_glyphs_dir))
    design_context.fallback(DesignContext.load(font_config, path_define.fallback_glyphs_dir))
    font_context = FontContext(design_context, width_mode)
    font_context.make_otf()
    font_context.make_woff2()
    font_context.make_ttf()
    font_context.make_bdf()
    font_context.make_pcf()
    font_context.make_otc()
    font_context.make_ttc()
    publish_service.make_release_zips(font_config, width_mode)
    info_service.make_info_file(design_context, width_mode)
    info_service.make_alphabet_txt_file(design_context, width_mode)


if __name__ == '__main__':
    main()
