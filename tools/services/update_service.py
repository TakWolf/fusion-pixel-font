import logging
import os
import shutil
import zipfile

from tools import configs
from tools.configs import path_define
from tools.configs.update import UpdateConfig
from tools.utils import fs_util, github_api, download_util

logger = logging.getLogger(__name__)


def update_ark_pixel_glyphs_version():
    repository_name = 'TakWolf/ark-pixel-font'
    source_type = 'tag'
    source_name = None

    if source_type == 'tag':
        tag_name = source_name
        if tag_name is None:
            tag_name = github_api.get_releases_latest_tag_name(repository_name)
        sha = github_api.get_tag_sha(repository_name, tag_name)
        version = tag_name
    elif source_type == 'branch':
        branch_name = source_name
        sha = github_api.get_branch_latest_commit_sha(repository_name, branch_name)
        version = branch_name
    elif source_type == 'commit':
        sha = source_name
        version = sha
    else:
        raise Exception(f"Unknown source type: '{source_type}'")
    version_info = {
        'sha': sha,
        'version': version,
        'version_url': f'https://github.com/{repository_name}/tree/{version}',
        'asset_url': f'https://github.com/{repository_name}/archive/{sha}.zip',
    }
    file_path = path_define.fonts_dir.joinpath('ark-pixel').joinpath('version.json')
    file_path.parent.mkdir(parents=True, exist_ok=True)
    fs_util.write_json(version_info, file_path)
    logger.info("Update version file: '%s'", file_path)


def setup_ark_pixel_glyphs():
    cache_version_file_path = path_define.ark_pixel_glyphs_dir.joinpath('version.json')
    if cache_version_file_path.is_file():
        cache_sha = fs_util.read_json(cache_version_file_path)['sha']
    else:
        cache_sha = None

    font_ark_pixel_dir = path_define.fonts_dir.joinpath('ark-pixel')
    version_file_path = font_ark_pixel_dir.joinpath('version.json')
    version_info = fs_util.read_json(version_file_path)
    sha = version_info['sha']
    if cache_sha == sha:
        return
    logger.info('Need setup glyphs')

    downloads_dir = path_define.downloads_dir.joinpath('ark-pixel-font')
    source_file_path = downloads_dir.joinpath(f'{sha}.zip')
    if not source_file_path.exists():
        asset_url = version_info['asset_url']
        logger.info("Start download: '%s'", asset_url)
        downloads_dir.mkdir(parents=True, exist_ok=True)
        download_util.download_file(asset_url, source_file_path)
    else:
        logger.info("Already downloaded: '%s'", source_file_path)

    source_unzip_dir = downloads_dir.joinpath(f'ark-pixel-font-{sha}')
    if source_unzip_dir.exists():
        shutil.rmtree(source_unzip_dir)
    with zipfile.ZipFile(source_file_path) as file:
        file.extractall(downloads_dir)
    logger.info("Unzip: '%s'", source_unzip_dir)

    if path_define.ark_pixel_glyphs_dir.exists():
        shutil.rmtree(path_define.ark_pixel_glyphs_dir)
    path_define.ark_pixel_glyphs_dir.mkdir(parents=True)
    for font_size in configs.font_sizes:
        source_glyphs_dir_from = source_unzip_dir.joinpath('assets', 'glyphs', str(font_size))
        source_glyphs_dir_to = path_define.ark_pixel_glyphs_dir.joinpath(str(font_size))
        if not source_glyphs_dir_from.is_dir():
            source_glyphs_dir_to.mkdir(parents=True)
            continue
        shutil.copytree(source_glyphs_dir_from, source_glyphs_dir_to)

        config_file_path_from = path_define.ark_pixel_glyphs_dir.joinpath(str(font_size), 'config.yml')
        config_file_path_to = path_define.patch_glyphs_dir.joinpath(str(font_size), 'config.yml')
        if config_file_path_to.exists():
            os.remove(config_file_path_to)
        config_file_path_to.parent.mkdir(parents=True, exist_ok=True)
        config_file_path_from.rename(config_file_path_to)

    license_path_from = source_unzip_dir.joinpath('LICENSE-OFL')
    license_path_to = font_ark_pixel_dir.joinpath('LICENSE.txt')
    shutil.copyfile(license_path_from, license_path_to)

    if source_unzip_dir.exists():
        shutil.rmtree(source_unzip_dir)
    fs_util.write_json(version_info, cache_version_file_path)
    logger.info("Update glyphs: '%s'", sha)


def update_fonts(update_config: UpdateConfig):
    if update_config.tag_name is None:
        tag_name = github_api.get_releases_latest_tag_name(update_config.repository_name)
    else:
        tag_name = update_config.tag_name
    logger.info("'%s' tag: '%s'", update_config.repository_name, tag_name)
    version = tag_name.removeprefix('v')

    fonts_dir = path_define.fonts_dir.joinpath(update_config.name)
    version_file_path = fonts_dir.joinpath('version.json')
    if version_file_path.exists():
        version_info = fs_util.read_json(version_file_path)
        if version == version_info['version']:
            return
    logger.info("Need update fonts: '%s'", update_config.name)

    repository_url = f'https://github.com/{update_config.repository_name}'
    downloads_dir = path_define.downloads_dir.joinpath(update_config.repository_name, tag_name)
    downloads_dir.mkdir(parents=True, exist_ok=True)

    if fonts_dir.exists():
        shutil.rmtree(fonts_dir)
    fonts_dir.mkdir(parents=True)

    for asset_config in update_config.asset_configs:
        if asset_config.file_name is None:
            asset_file_name = f'{tag_name}.zip'
            asset_url = f'{repository_url}/archive/refs/tags/{asset_file_name}'
        else:
            asset_file_name = asset_config.file_name.format(version=version)
            asset_url = f'{repository_url}/releases/download/{tag_name}/{asset_file_name}'
        asset_file_path = downloads_dir.joinpath(asset_file_name)
        if not asset_file_path.exists():
            logger.info("Start download: '%s'", asset_url)
            download_util.download_file(asset_url, asset_file_path)
        else:
            logger.info("Already downloaded: '%s'", asset_file_path)

        asset_unzip_dir = asset_file_path.with_suffix('')
        if asset_unzip_dir.exists():
            shutil.rmtree(asset_unzip_dir)
        with zipfile.ZipFile(asset_file_path) as file:
            file.extractall(asset_unzip_dir)
        logger.info("Unzip: '%s'", asset_unzip_dir)

        for copy_info in asset_config.copy_list:
            from_path = asset_unzip_dir.joinpath(copy_info[0].format(version=version))
            to_path = fonts_dir.joinpath(copy_info[1].format(version=version))
            shutil.copyfile(from_path, to_path)
            logger.info("Copy from '%s' to '%s'", from_path, to_path)
        if asset_unzip_dir.exists():
            shutil.rmtree(asset_unzip_dir)

    version_info = {
        'repository_url': repository_url,
        'version': version,
        'version_url': f'{repository_url}/releases/tag/{tag_name}',
    }
    version_file_path = fonts_dir.joinpath('version.json')
    fs_util.write_json(version_info, version_file_path)
    logger.info("Update version file: '%s'", version_file_path)
