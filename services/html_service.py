import logging
import os

import minify_html

import configs
from configs import path_define, font_config
from utils import fs_util

logger = logging.getLogger('html-service')


def make_alphabet_html_file(width_mode, alphabet):
    template = configs.template_env.get_template('alphabet.html')
    html = template.render(
        configs=configs,
        font_config=font_config,
        width_mode=width_mode,
        alphabet=''.join([c for c in alphabet if ord(c) >= 128]),
    )
    html = minify_html.minify(html, minify_css=True, minify_js=True)
    fs_util.make_dirs_if_not_exists(path_define.outputs_dir)
    html_file_path = os.path.join(path_define.outputs_dir, font_config.get_alphabet_html_file_name(width_mode))
    with open(html_file_path, 'w', encoding='utf-8') as file:
        file.write(html)
    logger.info(f'make {html_file_path}')


def make_index_html_file():
    template = configs.template_env.get_template('index.html')
    html = template.render(
        configs=configs,
        font_config=font_config,
    )
    html = minify_html.minify(html, minify_css=True, minify_js=True)
    fs_util.make_dirs_if_not_exists(path_define.outputs_dir)
    html_file_path = os.path.join(path_define.outputs_dir, 'index.html')
    with open(html_file_path, 'w', encoding='utf-8') as file:
        file.write(html)
    logger.info(f'make {html_file_path}')
