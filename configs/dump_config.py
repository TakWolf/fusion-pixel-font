import os

from configs import workspace_define


class DumpConfig:
    def __init__(self, name, font_file_path, px=12, offset_xy=(0, 0)):
        self.name = name
        self.font_path = os.path.join(workspace_define.fonts_dir, font_file_path)
        self.px = px
        self.offset_xy = offset_xy
