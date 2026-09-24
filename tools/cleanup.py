from tools.config import options
from tools.resource import setup_service, cleanup_service


def main() -> None:
    setup_service.setup_ark_pixel()

    for font_size in options.FONT_SIZES:
        cleanup_service.cleanup_cmap_glyphs(font_size)


if __name__ == '__main__':
    main()
