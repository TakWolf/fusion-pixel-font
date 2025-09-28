import json
import os
import shutil
import zipfile

from loguru import logger

from tools.configs import path_define
from tools.utils import download_util


def setup_ark_pixel():
    cache_version_file_path = path_define.cache_dir.joinpath('ark-pixel-version.json')
    if cache_version_file_path.is_file():
        cache_sha = json.loads(cache_version_file_path.read_bytes())['sha']
    else:
        cache_sha = None

    version_file_path = path_define.fonts_dir.joinpath('ark-pixel', 'version.json')
    version_info = json.loads(version_file_path.read_bytes())
    sha = version_info['sha']
    if cache_sha == sha:
        return
    logger.info('Need setup glyphs')

    downloads_dir = path_define.downloads_dir.joinpath('ark-pixel-font')
    source_file_path = downloads_dir.joinpath(f'{sha}.zip')
    if not source_file_path.exists():
        asset_url = version_info['asset_url']
        logger.info("Start download: '{}'", asset_url)
        downloads_dir.mkdir(parents=True, exist_ok=True)
        download_util.download_file(asset_url, source_file_path)
    else:
        logger.info("Already downloaded: '{}'", source_file_path)

    source_unzip_dir = downloads_dir.joinpath(f'ark-pixel-font-{sha}')
    if source_unzip_dir.exists():
        shutil.rmtree(source_unzip_dir)
    with zipfile.ZipFile(source_file_path) as file:
        file.extractall(downloads_dir)
    logger.info("Unzip: '{}'", source_unzip_dir)

    if path_define.ark_pixel_glyphs_dir.exists():
        shutil.rmtree(path_define.ark_pixel_glyphs_dir)
    source_unzip_dir.joinpath('assets', 'glyphs').rename(path_define.ark_pixel_glyphs_dir)

    if path_define.ark_pixel_configs_dir.exists():
        shutil.rmtree(path_define.ark_pixel_configs_dir)
    source_unzip_dir.joinpath('assets', 'configs').rename(path_define.ark_pixel_configs_dir)

    if path_define.ark_pixel_mappings_dir.exists():
        shutil.rmtree(path_define.ark_pixel_mappings_dir)
    source_unzip_dir.joinpath('assets', 'mappings').rename(path_define.ark_pixel_mappings_dir)

    if source_unzip_dir.exists():
        shutil.rmtree(source_unzip_dir)
    cache_version_file_path.write_text(f'{json.dumps(version_info, indent=2, ensure_ascii=False)}\n', 'utf-8')
    logger.info("Setup glyphs: '{}'", sha)
