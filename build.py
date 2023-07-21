import logging

import configs
from configs import path_define
from services import font_service, dump_service, publish_service, info_service, template_service, image_service
from utils import fs_util

logging.basicConfig(level=logging.DEBUG)


def main():
    fs_util.delete_dir(path_define.build_dir)

    for font_config in configs.font_configs:
        font_service.format_patch_glyph_files(font_config)
        base_context = font_service.collect_glyph_files(font_config, path_define.ark_pixel_glyphs_dir)
        base_context.patch(font_service.collect_glyph_files(font_config, path_define.patch_glyphs_dir))

        exclude_alphabet = set()
        for width_mode in configs.width_modes:
            exclude_alphabet.update(base_context.get_alphabet(width_mode))

        dump_configs = configs.font_size_to_dump_configs[font_config.size]
        for dump_config in dump_configs:
            dump_service.dump_font(dump_config, exclude_alphabet)

        fallback_configs = configs.font_size_to_fallback_configs[font_config.size]
        for fallback_config in fallback_configs:
            dump_service.apply_fallback(fallback_config)

        context = font_service.collect_glyph_files(font_config, path_define.fallback_glyphs_dir)
        context.patch(base_context)

        for width_mode in configs.width_modes:
            font_service.make_font_files(font_config, context, width_mode)
            publish_service.make_release_zips(font_config, width_mode)
            info_service.make_info_file(font_config, context, width_mode)
            info_service.make_alphabet_txt_file(font_config, context, width_mode)
            template_service.make_alphabet_html_file(font_config, context, width_mode)
        template_service.make_demo_html_file(font_config, context)
        image_service.make_preview_image_file(font_config)
    template_service.make_index_html_file()
    template_service.make_playground_html_file()


if __name__ == '__main__':
    main()
