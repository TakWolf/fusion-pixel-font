import itertools

from scripts import configs
from scripts.configs import path_define, FontConfig, DumpConfig, FallbackConfig
from scripts.services import update_service, dump_service, publish_service, info_service, template_service, image_service
from scripts.services.font_service import DesignContext, FontContext
from scripts.utils import fs_util


def main():
    fs_util.delete_dir(path_define.dump_dir)
    fs_util.delete_dir(path_define.fallback_glyphs_dir)
    fs_util.delete_dir(path_define.outputs_dir)
    fs_util.delete_dir(path_define.releases_dir)

    update_service.setup_ark_pixel_glyphs()

    font_configs = FontConfig.load_all()
    dump_configs = DumpConfig.load_all()
    fallback_configs = FallbackConfig.load_all()

    for font_size, font_config in font_configs.items():
        for dump_config in dump_configs[font_size]:
            dump_service.dump_font(dump_config)

        for fallback_config in fallback_configs[font_size]:
            dump_service.apply_fallback(fallback_config)

        design_context = DesignContext.load(font_config, path_define.patch_glyphs_dir)
        design_context.standardize()
        design_context.fallback(DesignContext.load(font_config, path_define.ark_pixel_glyphs_dir))
        design_context.fallback(DesignContext.load(font_config, path_define.fallback_glyphs_dir))
        for width_mode in configs.width_modes:
            font_context = FontContext(design_context, width_mode)
            font_context.make_otf()
            font_context.make_woff2()
            font_context.make_ttf()
            font_context.make_bdf()
            font_context.make_pcf()
            font_context.make_otc()
            font_context.make_ttc()
            for font_format in itertools.chain(configs.font_formats, configs.font_collection_formats):
                publish_service.make_release_zip(font_size, width_mode, font_format)
            info_service.make_info_file(design_context, width_mode)
            info_service.make_alphabet_txt_file(design_context, width_mode)
            template_service.make_alphabet_html_file(design_context, width_mode)
        template_service.make_demo_html_file(design_context)
        image_service.make_preview_image_file(font_config)
    template_service.make_index_html_file(font_configs)
    template_service.make_playground_html_file(font_configs)


if __name__ == '__main__':
    main()
