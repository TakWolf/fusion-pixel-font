import logging
import os.path
import shutil

import configs
from configs import workspace_define
from services import dump_service, font_service, info_service

logging.basicConfig(level=logging.DEBUG)


def main():
    if os.path.exists(workspace_define.dump_outputs_dir):
        shutil.rmtree(workspace_define.dump_outputs_dir)
    os.makedirs(workspace_define.dump_outputs_dir)

    design_dirs = [workspace_define.design_dir]
    for dump_config in configs.dump_configs:
        design_dirs.append(dump_service.dump_font(dump_config))

    if os.path.exists(workspace_define.outputs_dir):
        shutil.rmtree(workspace_define.outputs_dir)
    os.makedirs(workspace_define.outputs_dir)

    alphabet, design_file_paths = font_service.collect_design_files(design_dirs)
    font_service.make_fonts(alphabet, design_file_paths)
    info_service.make_info_file(alphabet)
    info_service.make_preview_image_file()
    info_service.make_alphabet_txt_file(alphabet)
    info_service.make_alphabet_html_file(alphabet)


if __name__ == '__main__':
    main()
