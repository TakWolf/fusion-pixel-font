import itertools
import shutil

from tools import configs
from tools.configs import path_define
from tools.configs.dump import DumpConfig
from tools.configs.fallback import FallbackConfig
from tools.configs.font import FontConfig
from tools.services import update_service, dump_service, publish_service, info_service, template_service, image_service
from tools.services.font_service import DesignContext, FontContext


def main():
    if path_define.build_dir.exists():
        shutil.rmtree(path_define.build_dir)

    update_service.setup_ark_pixel_glyphs()

    font_configs = {font_size: FontConfig.load(font_size) for font_size in configs.font_sizes}
    dump_configs = DumpConfig.load()
    fallback_configs = FallbackConfig.load()

    for font_size, font_config in font_configs.items():
        for dump_config in dump_configs[font_size]:
            dump_service.dump_font(dump_config)

        for fallback_config in fallback_configs[font_size]:
            dump_service.apply_fallback(fallback_config)

        design_context = DesignContext.load(font_config, path_define.patch_glyphs_dir)
        design_context.standardized()
        design_context.fallback(DesignContext.load(font_config, path_define.ark_pixel_glyphs_dir))
        design_context.fallback(DesignContext.load(font_config, path_define.fallback_glyphs_dir))
        for width_mode in configs.width_modes:
            font_context = FontContext(design_context, width_mode)
            for font_format in itertools.chain(configs.font_formats, configs.font_collection_formats):
                font_context.make_fonts(font_format)
                publish_service.make_release_zip(font_size, width_mode, font_format)
            info_service.make_font_info(design_context, width_mode)
            info_service.make_alphabet_txt(design_context, width_mode)
            template_service.make_alphabet_html(design_context, width_mode)
        template_service.make_demo_html(design_context)
        image_service.make_preview_image(font_config)
    template_service.make_index_html(font_configs)
    template_service.make_playground_html(font_configs)


if __name__ == '__main__':
    main()
