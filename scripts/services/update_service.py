import logging
import os
import shutil
import zipfile

from scripts import configs
from scripts.configs import path_define, ark_pixel_config, FontConfig, GitSourceType
from scripts.configs.update import UpdateConfig
from scripts.utils import fs_util, github_api, download_util

logger = logging.getLogger('update_service')


def update_ark_pixel_glyphs_version():
    if ark_pixel_config.source_type == GitSourceType.TAG:
        tag_name = ark_pixel_config.source_name
        if tag_name is None:
            tag_name = github_api.get_releases_latest_tag_name(ark_pixel_config.repository_name)
        sha = github_api.get_tag_sha(ark_pixel_config.repository_name, tag_name)
        version = tag_name
    elif ark_pixel_config.source_type == GitSourceType.BRANCH:
        branch_name = ark_pixel_config.source_name
        sha = github_api.get_branch_latest_commit_sha(ark_pixel_config.repository_name, branch_name)
        version = branch_name
    elif ark_pixel_config.source_type == GitSourceType.COMMIT:
        sha = ark_pixel_config.source_name
        version = sha
    else:
        raise Exception(f"Unknown source type: '{ark_pixel_config.source_type}'")
    version_info = {
        'sha': sha,
        'version': version,
        'version_url': f'https://github.com/{ark_pixel_config.repository_name}/tree/{version}',
        'asset_url': f'https://github.com/{ark_pixel_config.repository_name}/archive/{sha}.zip',
    }
    file_dir = os.path.join(path_define.fonts_dir, 'ark-pixel')
    fs_util.make_dir(file_dir)
    file_path = os.path.join(file_dir, 'version.json')
    fs_util.write_json(version_info, file_path)
    logger.info("Update version file: '%s'", file_path)


def setup_ark_pixel_glyphs():
    build_version_file_path = os.path.join(path_define.ark_pixel_glyphs_dir, 'version.json')
    if os.path.isfile(build_version_file_path):
        build_sha = fs_util.read_json(build_version_file_path)['sha']
    else:
        build_sha = None

    font_ark_pixel_dir = os.path.join(path_define.fonts_dir, 'ark-pixel')
    version_file_path = os.path.join(font_ark_pixel_dir, 'version.json')
    version_info = fs_util.read_json(version_file_path)
    sha = version_info['sha']
    if build_sha == sha:
        return
    logger.info('Need setup glyphs')

    download_dir = os.path.join(path_define.cache_dir, 'ark-pixel-font')
    source_file_path = os.path.join(download_dir, f'{sha}.zip')
    if not os.path.exists(source_file_path):
        asset_url = version_info['asset_url']
        logger.info("Start download: '%s'", asset_url)
        fs_util.make_dir(download_dir)
        download_util.download_file(asset_url, source_file_path)
    else:
        logger.info("Already downloaded: '%s'", source_file_path)

    source_unzip_dir = os.path.join(download_dir, f'ark-pixel-font-{sha}')
    fs_util.delete_dir(source_unzip_dir)
    with zipfile.ZipFile(source_file_path) as file:
        file.extractall(download_dir)
    logger.info("Unzip: '%s'", source_unzip_dir)

    fs_util.delete_dir(path_define.ark_pixel_glyphs_dir)
    fs_util.make_dir(path_define.ark_pixel_glyphs_dir)
    for font_config in configs.font_configs.values():
        source_glyphs_dir_from = os.path.join(source_unzip_dir, 'assets', 'glyphs', str(font_config.size))
        source_glyphs_dir_to = os.path.join(path_define.ark_pixel_glyphs_dir, str(font_config.size))
        if not os.path.isdir(source_glyphs_dir_from):
            fs_util.make_dir(source_glyphs_dir_to)
            continue
        shutil.copytree(source_glyphs_dir_from, source_glyphs_dir_to)

        config_file_path_from = os.path.join(path_define.ark_pixel_glyphs_dir, str(font_config.size), 'config.toml')
        config_file_path_to = os.path.join(path_define.patch_glyphs_dir, str(font_config.size), 'config.toml')
        os.remove(config_file_path_to)
        os.rename(config_file_path_from, config_file_path_to)

    license_path_from = os.path.join(source_unzip_dir, 'LICENSE-OFL')
    license_path_to = os.path.join(font_ark_pixel_dir, 'LICENSE.txt')
    shutil.copyfile(license_path_from, license_path_to)

    fs_util.delete_dir(source_unzip_dir)
    configs.font_configs = FontConfig.load_all()
    fs_util.write_json(version_info, build_version_file_path)
    logger.info("Update glyphs: '%s'", sha)


def update_fonts(update_config: UpdateConfig):
    if update_config.tag_name is None:
        tag_name = github_api.get_releases_latest_tag_name(update_config.repository_name)
    else:
        tag_name = update_config.tag_name
    logger.info("'%s' tag: '%s'", update_config.repository_name, tag_name)
    version = tag_name.removeprefix('v')

    fonts_dir = os.path.join(path_define.fonts_dir, update_config.name)
    version_file_path = os.path.join(fonts_dir, 'version.json')
    version_info = fs_util.read_json(version_file_path)
    if version == version_info['version']:
        return
    logger.info("Need update fonts: '%s'", update_config.name)

    repository_url = f'https://github.com/{update_config.repository_name}'
    download_dir = os.path.join(path_define.cache_dir, update_config.repository_name, tag_name)
    fs_util.make_dir(download_dir)

    fs_util.delete_dir(fonts_dir)
    fs_util.make_dir(fonts_dir)

    for asset_config in update_config.asset_configs:
        asset_file_name = asset_config.file_name.format(version=version)
        asset_file_path = os.path.join(download_dir, asset_file_name)
        if not os.path.exists(asset_file_path):
            asset_url = f'{repository_url}/releases/download/{tag_name}/{asset_file_name}'
            logger.info("Start download: '%s'", asset_url)
            download_util.download_file(asset_url, asset_file_path)
        else:
            logger.info("Already downloaded: '%s'", asset_file_path)

        asset_unzip_dir = asset_file_path.removesuffix('.zip')
        fs_util.delete_dir(asset_unzip_dir)
        with zipfile.ZipFile(asset_file_path) as file:
            file.extractall(asset_unzip_dir)
        logger.info("Unzip: '%s'", asset_unzip_dir)

        for copy_info in asset_config.copy_list:
            from_path = os.path.join(asset_unzip_dir, copy_info[0].format(version=version))
            to_path = os.path.join(fonts_dir, copy_info[1].format(version=version))
            shutil.copyfile(from_path, to_path)
            logger.info("Copy from '%s' to '%s'", from_path, to_path)
        fs_util.delete_dir(asset_unzip_dir)

    version_info = {
        'repository_url': repository_url,
        'version': version,
        'version_url': f'{repository_url}/releases/tag/{tag_name}',
    }
    version_file_path = os.path.join(fonts_dir, 'version.json')
    fs_util.write_json(version_info, version_file_path)
    logger.info("Update version file: '%s'", version_file_path)
