from tools.config import options
from tools.config.font import FontConfig
from tools.extra import image_service


def main() -> None:
    for font_size in options.FONT_SIZES:
        font_config = FontConfig.load(font_size)

        image_service.make_preview_image(font_config)


if __name__ == '__main__':
    main()
