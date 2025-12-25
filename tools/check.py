from tools.configs import options
from tools.services import setup_service, check_service


def main():
    setup_service.setup_ark_pixel()

    for font_size in options.font_sizes:
        check_service.check_glyphs(font_size)


if __name__ == '__main__':
    main()
