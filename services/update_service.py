import json
import logging
import os
import shutil
import zipfile

import requests

from configs import path_define
from utils import fs_util

logger = logging.getLogger('update-service')


def _get_github_releases_latest_tag_name(repository_name):
    url = f'https://api.github.com/repos/{repository_name}/releases/latest'
    response = requests.get(url)
    assert response.ok, repository_name
    return response.json()['tag_name']


def _do_download_file(url, file_path):
    response = requests.get(url, stream=True)
    assert response.ok, url
    tmp_file_path = f'{file_path}.download'
    with open(tmp_file_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=512):
            if chunk is not None:
                file.write(chunk)
    os.rename(tmp_file_path, file_path)


def update_font(download_config):
    if download_config.tag_name is None:
        tag_name = _get_github_releases_latest_tag_name(download_config.repository_name)
    else:
        tag_name = download_config.tag_name
    logger.info(f'{download_config.name} tag: {tag_name}')

    repository_url = f'https://github.com/{download_config.repository_name}'
    version = tag_name.removeprefix('v')
    version_url = f'{repository_url}/releases/tag/{tag_name}'
    asset_file_name = download_config.asset_file_name.format(version=version)
    asset_url = f'{repository_url}/releases/download/{tag_name}/{asset_file_name}'

    download_dir = os.path.join(path_define.cache_dir, download_config.name, tag_name)
    asset_file_path = os.path.join(download_dir, asset_file_name)
    if not os.path.exists(asset_file_path):
        logger.info(f'start download {asset_url}')
        fs_util.make_dirs_if_not_exists(download_dir)
        _do_download_file(asset_url, asset_file_path)
    else:
        logger.info(f'{asset_file_path} already exists')

    asset_unzip_dir = asset_file_path.removesuffix('.zip')
    fs_util.delete_dir(asset_unzip_dir)
    with zipfile.ZipFile(asset_file_path) as zip_file:
        zip_file.extractall(asset_unzip_dir)
    logger.info(f'unzip {asset_unzip_dir}')

    font_dir = os.path.join(path_define.fonts_dir, download_config.name)
    fs_util.delete_dir(font_dir)
    os.makedirs(font_dir)
    font_from_path = os.path.join(asset_unzip_dir, download_config.font_file_path.format(version=version))
    font_file_name = os.path.basename(font_from_path)
    font_to_path = os.path.join(font_dir, font_file_name)
    shutil.copyfile(font_from_path, font_to_path)
    ofl_txt_from_path = os.path.join(asset_unzip_dir, download_config.ofl_file_path.format(version=version))
    ofl_txt_to_path = os.path.join(font_dir, 'OFL.txt')
    shutil.copyfile(ofl_txt_from_path, ofl_txt_to_path)
    logger.info(f'update font files {font_dir}')

    version_info = {
        'font_name': download_config.font_name,
        'repository_url': repository_url,
        'version': version,
        'version_url': version_url,
        'asset_url': asset_url,
        'font_file_name': font_file_name,
    }
    version_info_file_path = os.path.join(font_dir, 'version.json')
    with open(version_info_file_path, 'w', encoding='utf-8') as file:
        file.write(json.dumps(version_info, indent=2, ensure_ascii=False))
        file.write('\n')
    logger.info(f'make {version_info_file_path}')
