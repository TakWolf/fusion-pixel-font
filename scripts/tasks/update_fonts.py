from fontTools.ttLib import TTFont

from scripts.configs import path_define
from scripts.configs.update import UpdateConfig
from scripts.services import update_service


def main():
    update_service.update_ark_pixel_glyphs_version()
    update_service.setup_ark_pixel_glyphs()

    update_configs = UpdateConfig.load_all()
    for update_config in update_configs:
        update_service.update_fonts(update_config)

    # TODO
    # https://github.com/ItMarki/MisekiBitmap/issues/3
    # 「美績点陣體」的位图层字形映射错乱，这里主动将其删除，以保证栅格化正确
    font_file_path = path_define.fonts_dir.joinpath('miseki-bitmap', 'MisekiBitmap.ttf')
    font = TTFont(font_file_path)
    font.reader.tables.pop('EBLC', None)
    font.reader.tables.pop('EBDT', None)
    font.save(font_file_path)


if __name__ == '__main__':
    main()
