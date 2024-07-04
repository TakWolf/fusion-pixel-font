from pathlib import Path

from tools import configs
from tools.configs import path_define
from tools.utils import fs_util


class DumpConfig:
    @staticmethod
    def load() -> dict[int, list['DumpConfig']]:
        configs_data = fs_util.read_yaml(path_define.assets_dir.joinpath('dump-configs.yml'))
        dump_configs = {font_size: [] for font_size in configs.font_sizes}
        for name, items_data in configs_data.items():
            version = fs_util.read_json(path_define.fonts_dir.joinpath(name, 'version.json'))['version']
            for item_data in items_data:
                font_file_path = path_define.fonts_dir.joinpath(name, item_data['font-file-name'].format(version=version))
                font_size = item_data['font-size']
                dump_dir = path_define.dump_dir.joinpath(str(font_size), item_data['dump-dir-name'])
                rasterize_size = item_data.get('rasterize-size', font_size)
                rasterize_offset_x = item_data.get('rasterize-offset-x', 0)
                rasterize_offset_y = item_data.get('rasterize-offset-y', 0)
                dump_configs[font_size].append(DumpConfig(
                    name,
                    font_file_path,
                    font_size,
                    dump_dir,
                    rasterize_size,
                    rasterize_offset_x,
                    rasterize_offset_y,
                ))
        return dump_configs

    name: str
    font_file_path: Path
    font_size: int
    dump_dir: Path
    rasterize_size: int
    rasterize_offset_x: int
    rasterize_offset_y: int

    def __init__(
            self,
            name: str,
            font_file_path: Path,
            font_size: int,
            dump_dir: Path,
            rasterize_size: int,
            rasterize_offset_x: int,
            rasterize_offset_y: int,
    ):
        self.name = name
        self.font_file_path = font_file_path
        self.font_size = font_size
        self.dump_dir = dump_dir
        self.rasterize_size = rasterize_size
        self.rasterize_offset_x = rasterize_offset_x
        self.rasterize_offset_y = rasterize_offset_y

    @property
    def rasterize_offset(self) -> tuple[int, int]:
        return self.rasterize_offset_x, self.rasterize_offset_y
