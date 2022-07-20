import logging
import os
import shutil
import time

import git

import configs
from configs import workspace_define

logger = logging.getLogger('publish-service')


def _copy_file(file_name, from_dir, to_dir):
    from_path = os.path.join(from_dir, file_name)
    to_path = os.path.join(to_dir, file_name)
    shutil.copyfile(from_path, to_path)
    logger.info(f'copy from {from_path} to {to_path}')


def copy_release_files():
    file_names = [
        'fusion-pixel.otf',
        'fusion-pixel.ttf',
        'fusion-pixel.woff2',
    ]
    for file_name in file_names:
        _copy_file(file_name, workspace_define.outputs_dir, workspace_define.releases_dir)


def copy_docs_files():
    file_names = [
        'font-info.md',
        'preview.png',
    ]
    for file_name in file_names:
        _copy_file(file_name, workspace_define.outputs_dir, workspace_define.docs_dir)


def copy_www_files():
    file_names = [
        'fusion-pixel.woff2',
        'alphabet.html',
    ]
    for file_name in file_names:
        _copy_file(file_name, workspace_define.outputs_dir, workspace_define.www_dir)


def deploy_www():
    repo = git.Repo.init(workspace_define.www_dir)
    repo.git.add(all=True)
    repo.git.commit(m=f'deployed at {time.strftime("%Y-%m-%d %H-%M-%S")}')
    current_branch_name = repo.git.branch(show_current=True)
    for git_deploy_config in configs.git_deploy_configs:
        repo.git.remote('add', git_deploy_config.remote_name, git_deploy_config.url)
        repo.git.push(git_deploy_config.remote_name, f'{current_branch_name}:{git_deploy_config.branch_name}', '-f')
