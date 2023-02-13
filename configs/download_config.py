
class DownloadConfig:
    def __init__(self, name, font_name, repository_name, tag_name, asset_file_name, font_file_path, ofl_file_path, is_enabled=True):
        self.name = name
        self.font_name = font_name
        self.repository_name = repository_name
        self.tag_name = tag_name
        self.asset_file_name = asset_file_name
        self.font_file_path = font_file_path
        self.ofl_file_path = ofl_file_path
        self.is_enabled = is_enabled
