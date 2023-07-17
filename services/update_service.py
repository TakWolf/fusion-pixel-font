import json
import logging
import os
import shutil
import zipfile

import requests

from configs import path_define
from configs.update_config import UpdateConfig
from utils import fs_util

logger = logging.getLogger('update-service')


def _get_github_releases_latest_tag_name(repository_name: str) -> str:
    url = f'https://api.github.com/repos/{repository_name}/releases/latest'
    response = requests.get(url)
    assert response.ok, url
    return response.json()['tag_name']


def _get_github_branch_latest_commit_sha(repository_name: str, branch_name: str) -> str:
    url = f'https://api.github.com/repos/{repository_name}/branches/{branch_name}'
    response = requests.get(url)
    assert response.ok, url
    return response.json()['commit']['sha']


def _download_file(url: str, file_path: str):
    response = requests.get(url, stream=True)
    assert response.ok, url
    tmp_file_path = f'{file_path}.download'
    with open(tmp_file_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=512):
            if chunk is not None:
                file.write(chunk)
    os.rename(tmp_file_path, file_path)


def update_fonts(update_config: UpdateConfig):
    if update_config.tag_name is None:
        tag_name = _get_github_releases_latest_tag_name(update_config.repository_name)
    else:
        tag_name = update_config.tag_name
    logger.info(f'{update_config.repository_name} tag: {tag_name}')

    version = tag_name.removeprefix('v')
    repository_url = f'https://github.com/{update_config.repository_name}'

    download_dir = os.path.join(path_define.cache_dir, update_config.repository_name, tag_name)
    fs_util.make_dirs(download_dir)

    fonts_dir = os.path.join(path_define.fonts_dir, update_config.name)
    fs_util.delete_dir(fonts_dir)
    os.makedirs(fonts_dir)

    for asset_config in update_config.asset_configs:
        asset_file_name = asset_config.file_name.format(version=version)
        asset_file_path = os.path.join(download_dir, asset_file_name)
        if not os.path.exists(asset_file_path):
            asset_url = f'{repository_url}/releases/download/{tag_name}/{asset_file_name}'
            logger.info(f"Start download: '{asset_url}'")
            _download_file(asset_url, asset_file_path)
        else:
            logger.info(f"Already downloaded: '{asset_file_path}'")

        asset_unzip_dir = asset_file_path.removesuffix('.zip')
        fs_util.delete_dir(asset_unzip_dir)
        with zipfile.ZipFile(asset_file_path) as file:
            file.extractall(asset_unzip_dir)
        logger.info(f"Unzip: '{asset_unzip_dir}'")

        for copy_info in asset_config.copy_list:
            from_path = os.path.join(asset_unzip_dir, copy_info[0].format(version=version))
            to_path = os.path.join(fonts_dir, copy_info[1].format(version=version))
            shutil.copyfile(from_path, to_path)
            logger.info(f"Copy from '{from_path}' to '{to_path}'")
        fs_util.delete_dir(asset_unzip_dir)

    version_info = {
        'repository_url': repository_url,
        'version': version,
        'version_url': f'{repository_url}/releases/tag/{tag_name}',
    }
    version_info_file_path = os.path.join(fonts_dir, 'version.json')
    with open(version_info_file_path, 'w', encoding='utf-8') as file:
        file.write(json.dumps(version_info, indent=2, ensure_ascii=False))
        file.write('\n')
    logger.info(f"Make version info file: '{version_info_file_path}'")
