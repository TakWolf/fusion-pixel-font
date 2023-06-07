import json
import logging
import os

from jinja2 import Environment, FileSystemLoader

import configs
from configs import path_define, font_config, ark_pixel_config
from utils import fs_util

logger = logging.getLogger('template-service')

_environment = Environment(
    trim_blocks=True,
    lstrip_blocks=True,
    loader=FileSystemLoader(path_define.templates_dir),
)


def make_alphabet_html_file(width_mode, alphabet):
    template = _environment.get_template('alphabet.html')
    html = template.render(
        configs=configs,
        font_config=font_config,
        width_mode=width_mode,
        alphabet=''.join([c for c in alphabet if ord(c) >= 128]),
    )
    fs_util.make_dirs(path_define.outputs_dir)
    html_file_path = os.path.join(path_define.outputs_dir, font_config.get_alphabet_html_file_name(width_mode))
    with open(html_file_path, 'w', encoding='utf-8') as file:
        file.write(html)
    logger.info(f'make {html_file_path}')


def make_index_html_file():
    template = _environment.get_template('index.html')
    html = template.render(
        configs=configs,
        font_config=font_config,
    )
    fs_util.make_dirs(path_define.outputs_dir)
    html_file_path = os.path.join(path_define.outputs_dir, 'index.html')
    with open(html_file_path, 'w', encoding='utf-8') as file:
        file.write(html)
    logger.info(f'make {html_file_path}')


def _read_json_file(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.loads(file.read())
    return data


def make_readme_md_file():
    fallback_infos = ''
    fallback_infos += '| 字体 | 版本 | 文件 |\n'
    fallback_infos += '|---|---|---|\n'
    ark_pixel_version_info = _read_json_file(os.path.join(path_define.fonts_dir, 'ark-pixel-monospaced', 'version.json'))
    fallback_infos += f'| [方舟像素字体]({ark_pixel_version_info["repository_url"]}) | [{ark_pixel_version_info["version"]}]({ark_pixel_version_info["version_url"]}) | 12px-{ark_pixel_config.language_specific}.otf |\n'
    for fallback_name in configs.fallback_names:
        version_info = _read_json_file(os.path.join(path_define.fonts_dir, fallback_name, 'version.json'))
        fallback_infos += f'| [{version_info["font_name"]}]({version_info["repository_url"]}) | [{version_info["version"]}]({version_info["version_url"]}) | {version_info["font_file_name"]} |\n'
    fallback_infos = fallback_infos.strip()

    template = _environment.get_template('README.md')
    markdown = template.render(fallback_infos=fallback_infos)
    md_file_path = os.path.join(path_define.project_root_dir, 'README.md')
    with open(md_file_path, 'w', encoding='utf-8') as file:
        file.write(markdown)
        file.write('\n')
    logger.info(f'make {md_file_path}')
