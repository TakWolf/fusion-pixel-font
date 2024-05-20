import os

from scripts import configs
from scripts.configs import path_define
from scripts.utils import fs_util


class DumpConfig:
    @staticmethod
    def load_all() -> dict[int, list['DumpConfig']]:
        configs_data = fs_util.read_yaml(os.path.join(path_define.assets_dir, 'dump-configs.yaml'))
        dump_configs = {font_size: [] for font_size in configs.font_sizes}
        for name, items_data in configs_data.items():
            version = fs_util.read_json(os.path.join(path_define.fonts_dir, name, 'version.json'))['version']
            for item_data in items_data:
                font_file_path = os.path.join(path_define.fonts_dir, name, item_data['font_file_name'].format(version=version))
                font_size = item_data['font_size']
                dump_dir = os.path.join(path_define.dump_dir, str(font_size), item_data['dump_dir_name'])
                rasterize_size = item_data.get('rasterize_size', font_size)
                rasterize_offset_x = item_data.get('rasterize_offset_x', 0)
                rasterize_offset_y = item_data.get('rasterize_offset_y', 0)
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
    font_file_path: str
    font_size: int
    dump_dir: str
    rasterize_size: int
    rasterize_offset_x: int
    rasterize_offset_y: int

    def __init__(
            self,
            name: str,
            font_file_path: str,
            font_size: int,
            dump_dir: str,
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
