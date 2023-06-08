
class DumpConfig:
    def __init__(
            self,
            font_file_name: str,
            font_size: int,
            width_mode_dir_name: str,
            rasterize_font_size: int = None,
            rasterize_offset: tuple[int, int] = (0, 0),
    ):
        self.font_file_name = font_file_name
        self.font_size = font_size
        self.width_mode_dir_name = width_mode_dir_name
        if rasterize_font_size is None:
            rasterize_font_size = font_size
        self.rasterize_font_size = rasterize_font_size
        self.rasterize_offset = rasterize_offset
