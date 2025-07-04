import json
import shutil
import zipfile

from loguru import logger

from tools.configs import path_define, UpgradeConfig
from tools.utils import github_api, download_util


def upgrade_ark_pixel():
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
    file_path.write_text(f'{json.dumps(version_info, indent=2, ensure_ascii=False)}\n', 'utf-8')
    logger.info("Update version file: '{}'", file_path)


def upgrade_fonts(upgrade_config: UpgradeConfig):
    if upgrade_config.tag_name is None:
        tag_name = github_api.get_releases_latest_tag_name(upgrade_config.repository_name)
    else:
        tag_name = upgrade_config.tag_name
    logger.info("'{}' tag: '{}'", upgrade_config.repository_name, tag_name)
    version = tag_name.removeprefix('v')

    fonts_dir = path_define.fonts_dir.joinpath(upgrade_config.name)
    version_file_path = fonts_dir.joinpath('version.json')
    if version_file_path.exists():
        version_info = json.loads(version_file_path.read_bytes())
        if version == version_info['version']:
            return
    logger.info("Need upgrade fonts: '{}'", upgrade_config.name)

    repository_url = f'https://github.com/{upgrade_config.repository_name}'
    downloads_dir = path_define.downloads_dir.joinpath(upgrade_config.repository_name, tag_name)
    downloads_dir.mkdir(parents=True, exist_ok=True)

    if fonts_dir.exists():
        shutil.rmtree(fonts_dir)
    fonts_dir.mkdir(parents=True)

    for asset_config in upgrade_config.asset_configs:
        if asset_config.file_name is None:
            asset_file_name = f'{tag_name}.zip'
            asset_url = f'{repository_url}/archive/refs/tags/{asset_file_name}'
        else:
            asset_file_name = asset_config.file_name.format(version=version)
            asset_url = f'{repository_url}/releases/download/{tag_name}/{asset_file_name}'
        asset_file_path = downloads_dir.joinpath(asset_file_name)
        if not asset_file_path.exists():
            logger.info("Start download: '{}'", asset_url)
            download_util.download_file(asset_url, asset_file_path)
        else:
            logger.info("Already downloaded: '{}'", asset_file_path)

        asset_unzip_dir = asset_file_path.with_suffix('')
        if asset_unzip_dir.exists():
            shutil.rmtree(asset_unzip_dir)
        with zipfile.ZipFile(asset_file_path) as file:
            file.extractall(asset_unzip_dir)
        logger.info("Unzip: '{}'", asset_unzip_dir)

        for copy_info in asset_config.copy_list:
            from_path = asset_unzip_dir.joinpath(copy_info[0].format(version=version))
            to_path = fonts_dir.joinpath(copy_info[1].format(version=version))
            shutil.copyfile(from_path, to_path)
            logger.info("Copy from '{}' to '{}'", from_path, to_path)
        if asset_unzip_dir.exists():
            shutil.rmtree(asset_unzip_dir)

    version_info = {
        'repository_url': repository_url,
        'version': version,
        'version_url': f'{repository_url}/releases/tag/{tag_name}',
    }
    version_file_path = fonts_dir.joinpath('version.json')
    version_file_path.write_text(f'{json.dumps(version_info, indent=2, ensure_ascii=False)}\n', 'utf-8')
    logger.info("Update version file: '{}'", version_file_path)
