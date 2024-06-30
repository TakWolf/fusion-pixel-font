from tools.configs import path_define, DumpConfig
from tools.services import dump_service
from tools.utils import fs_util


def main():
    fs_util.delete_dir(path_define.dump_dir)

    for dump_configs in DumpConfig.load_all().values():
        for dump_config in dump_configs:
            dump_service.dump_font(dump_config)


if __name__ == '__main__':
    main()
