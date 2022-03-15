from configs.dump_config import DumpConfig
from configs.git_deploy_config import GitDeployConfig

dump_configs = [
    DumpConfig(
        'ark-pixel-zh_cn',
        'ark-pixel/ark-pixel-12px-zh_cn.otf',
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

git_deploy_configs = [GitDeployConfig(
    'git@github.com:TakWolf/fusion-pixel-font.git',
    'github',
    'gh-pages',
)]
