from scripts import configs
from scripts.configs import path_define
from scripts.services import font_service, dump_service
from scripts.utils import fs_util


def main():
    fs_util.delete_dir(path_define.dump_dir)

    for font_config in configs.font_configs.values():
        font_service.format_patch_glyph_files(font_config)
        base_context = font_service.collect_glyph_files(font_config, path_define.ark_pixel_glyphs_dir)
        base_context.patch(font_service.collect_glyph_files(font_config, path_define.patch_glyphs_dir))

        exclude_alphabet = set()
        for width_mode in configs.width_modes:
            exclude_alphabet.update(base_context.get_alphabet(width_mode))

        dump_configs = configs.font_size_to_dump_configs[font_config.size]
        for dump_config in dump_configs:
            dump_service.dump_font(dump_config, exclude_alphabet)


if __name__ == '__main__':
    main()
