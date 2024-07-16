from tools import configs
from tools.configs.dump import DumpConfig
from tools.configs.fallback import FallbackConfig
from tools.configs.font import FontConfig
from tools.services import update_service, dump_service, template_service
from tools.services.font_service import DesignContext


def main():
    update_service.setup_ark_pixel_glyphs()

    dump_configs = DumpConfig.load()
    fallback_configs = FallbackConfig.load()
    font_configs = {}

    for font_size in configs.font_sizes:
        for dump_config in dump_configs[font_size]:
            dump_service.dump_font(dump_config)

        for fallback_config in fallback_configs[font_size]:
            dump_service.apply_fallback(fallback_config)

        font_config = FontConfig.load(font_size)
        font_configs[font_size] = font_config
        design_context = DesignContext.load(font_config)
        for width_mode in configs.width_modes:
            design_context.make_fonts(width_mode, 'woff2')
            template_service.make_alphabet_html(design_context, width_mode)
        template_service.make_demo_html(design_context)
    template_service.make_index_html(font_configs)
    template_service.make_playground_html(font_configs)


if __name__ == '__main__':
    main()
