from tools.configs import options
from tools.configs.font import FontConfig
from tools.services import format_service


def main():
    for font_size in options.font_sizes:
        font_config = FontConfig.load(font_size)
        format_service.format_glyphs(font_config)


if __name__ == '__main__':
    main()
