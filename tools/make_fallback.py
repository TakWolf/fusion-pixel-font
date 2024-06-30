from tools.configs import path_define, FallbackConfig
from tools.services import dump_service
from tools.utils import fs_util


def main():
    fs_util.delete_dir(path_define.fallback_glyphs_dir)

    for fallback_configs in FallbackConfig.load_all().values():
        for fallback_config in fallback_configs:
            dump_service.apply_fallback(fallback_config)


if __name__ == '__main__':
    main()
