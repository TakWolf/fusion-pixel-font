from scripts import configs
from scripts.configs import path_define
from scripts.services import update_service, dump_service, publish_service, info_service
from scripts.services.font_service import DesignContext, FontContext


def main():
    update_service.setup_ark_pixel_glyphs()

    font_config = configs.font_configs[12]
    design_context = DesignContext.load(font_config, path_define.patch_glyphs_dir)
    design_context.standardize()
    design_context.fallback(DesignContext.load(font_config, path_define.ark_pixel_glyphs_dir))

    exclude_alphabet = set()
    for width_mode in configs.width_modes:
        exclude_alphabet.update(design_context.get_alphabet(width_mode))

    dump_configs = configs.dump_configs[font_config.font_size]
    for dump_config in dump_configs:
        dump_service.dump_font(dump_config, exclude_alphabet)

    fallback_configs = configs.fallback_configs[font_config.font_size]
    for fallback_config in fallback_configs:
        dump_service.apply_fallback(fallback_config)

    design_context.fallback(DesignContext.load(font_config, path_define.fallback_glyphs_dir))

    width_mode = 'monospaced'
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
