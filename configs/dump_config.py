import json
import os

from configs import path_define


class DumpConfig:
    def __init__(self, name, px=12, offset_xy=(0, 0)):
        self.name = name
        self.px = px
        self.offset_xy = offset_xy
        self._version_info = None

    def _load_version_info(self):
        if self._version_info is None:
            version_info_file_path = os.path.join(path_define.fonts_dir, self.name, 'version.json')
            with open(version_info_file_path, 'r', encoding='utf-8') as file:
                self._version_info = json.loads(file.read())

    def get_font_file_path(self):
        self._load_version_info()
        return os.path.join(path_define.fonts_dir, self.name, self._version_info['font_file_name'])
