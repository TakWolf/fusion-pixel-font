import logging
import os.path
import shutil

import configs
from configs import workspace_define
from services import dump_service

logging.basicConfig(level=logging.DEBUG)


def main():
    if os.path.exists(workspace_define.dump_outputs_dir):
        shutil.rmtree(workspace_define.dump_outputs_dir)

    for dump_config in configs.dump_configs:
        dump_service.dump_font(dump_config)


if __name__ == '__main__':
    main()
