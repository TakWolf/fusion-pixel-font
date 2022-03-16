import os

from jinja2 import Environment, FileSystemLoader

from configs import workspace_define
from configs.dump_config import DumpConfig
from configs.git_deploy_config import GitDeployConfig
from utils import unicode_util

target_px = 12

dump_configs = [
    DumpConfig(
        'ark-pixel',
        'ark-pixel/ark-pixel-12px-zh_tr.otf',
    ),
    DumpConfig(
        'Galmuri-11',
        'Galmuri/Galmuri11.ttf',
        offset_xy=(0, -2),
    ),
    DumpConfig(
        'Cubic-11',
        'Cubic-11/Cubic_11_1.010_r.ttf',
        offset_xy=(-1, 0),
    ),
]

font_config = (12, 10)

unicode_blocks = unicode_util.load_blocks_db(os.path.join(workspace_define.unidata_dir, 'blocks.txt'))

template_env = Environment(loader=FileSystemLoader(workspace_define.templates_dir))

git_deploy_configs = [GitDeployConfig(
    'git@github.com:TakWolf/fusion-pixel-font.git',
    'github',
    'gh-pages',
)]
