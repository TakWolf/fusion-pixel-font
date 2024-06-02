from scripts import configs
from scripts.configs import path_define, FontConfig, DumpConfig
from scripts.services import dump_service
from scripts.services.font_service import DesignContext
from scripts.utils import fs_util


def main():
    fs_util.delete_dir(path_define.dump_dir)

    font_configs = FontConfig.load_all()
    dump_configs = DumpConfig.load_all()

    for font_size, font_config in font_configs.items():
        design_context = DesignContext.load(font_config, path_define.patch_glyphs_dir)
        design_context.standardize()
        design_context.fallback(DesignContext.load(font_config, path_define.ark_pixel_glyphs_dir))

        exclude_alphabet = set()
        for width_mode in configs.width_modes:
            exclude_alphabet.update(design_context.get_alphabet(width_mode))

        for dump_config in dump_configs[font_size]:
            dump_service.dump_font(dump_config, exclude_alphabet)


if __name__ == '__main__':
    main()
