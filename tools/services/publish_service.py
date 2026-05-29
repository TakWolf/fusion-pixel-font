import re
import zipfile

from loguru import logger

from tools import configs
from tools.configs import path_define, options
from tools.configs.options import FontSize, WidthMode, FontFormat


def make_release_zips(font_size: FontSize, width_mode: WidthMode, font_formats: list[FontFormat]):
    path_define.releases_dir.mkdir(parents=True, exist_ok=True)

    for font_format in font_formats:
        file_path = path_define.releases_dir.joinpath(f'fusion-pixel-font-{font_size}px-{width_mode}-{font_format}-v{configs.version}.zip')
        with zipfile.ZipFile(file_path, 'w') as file:
            file.write(path_define.project_root_dir.joinpath('LICENSE-OFL'), 'OFL.txt')

            for font_name, file_names in sorted(configs.license_configs[font_size].items()):
                for file_name in file_names:
                    file.write(path_define.fonts_dir.joinpath(font_name, file_name), f'LICENSES/{font_name}/{file_name}')

            for language_flavor in options.language_flavors:
                font_file_name = f'fusion-pixel-{font_size}px-{width_mode}-{language_flavor}.{font_format}'
                file.write(path_define.outputs_dir.joinpath(font_file_name), font_file_name)
        logger.info("Make release zip: '{}'", file_path)


def update_docs():
    path_define.docs_dir.mkdir(parents=True, exist_ok=True)

    regex_file_name = re.compile(r'^(info-.*px-.*\.md|preview-.*px\.png)$')
    for path_from in path_define.outputs_dir.iterdir():
        if regex_file_name.match(path_from.name) is None:
            continue
        path_to = path_from.copy_into(path_define.docs_dir)
        logger.info("Copy file: '{}' -> '{}'", path_from, path_to)
