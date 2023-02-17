import os
import time
import tomllib

from configs import path_define

display_name_prefix = 'Fusion Pixel'
unique_name_prefix = 'Fusion-Pixel'
output_name_prefix = 'fusion-pixel'
style_name = 'Regular'
version = f'{time.strftime("%Y.%m.%d")}'
copyright_string = 'Copyright (c) 2022, TakWolf (https://takwolf.com), with Reserved Font Name "Fusion Pixel".'
designer = 'TakWolf'
description = 'Open source pixel font.'
vendor_url = 'https://fusion-pixel-font.takwolf.com'
designer_url = 'https://takwolf.com'
license_description = 'This Font Software is licensed under the SIL Open Font License, Version 1.1.'
license_info_url = 'https://scripts.sil.org/OFL'


class FontAttrs:
    def __init__(self, config_data):
        self.box_origin_y_px = config_data['box_origin_y_px']
        self.x_height_px = config_data['x_height_px']
        self.cap_height_px = config_data['cap_height_px']


class VerticalMetrics:
    def __init__(self, ascent, descent, x_height, cap_height):
        self.ascent = ascent
        self.descent = descent
        self.x_height = x_height
        self.cap_height = cap_height


config_file_path = os.path.join(path_define.fonts_dir, 'config.toml')
with open(config_file_path, 'rb') as config_file:
    config_data = tomllib.load(config_file)['font']

px = config_data['px']
display_line_height_px = config_data['display_line_height_px']
assert (display_line_height_px - px) % 2 == 0, f'font_config {px}px with incorrect display_line_height_px {display_line_height_px}px'
monospaced_attrs = FontAttrs(config_data['monospaced'])
proportional_attrs = FontAttrs(config_data['proportional'])
px_units = 100


def get_units_per_em():
    return px * px_units


def get_box_origin_y(width_mode):
    if width_mode == 'monospaced':
        attrs = monospaced_attrs
    else:  # proportional
        attrs = proportional_attrs
    return attrs.box_origin_y_px * px_units


def get_vertical_metrics(width_mode):
    if width_mode == 'monospaced':
        line_height_px = px
        attrs = monospaced_attrs
    else:  # proportional
        line_height_px = display_line_height_px
        attrs = proportional_attrs
    ascent = (attrs.box_origin_y_px + int((line_height_px - px) / 2)) * px_units
    descent = ascent - line_height_px * px_units
    x_height = attrs.x_height_px * px_units
    cap_height = attrs.cap_height_px * px_units
    return VerticalMetrics(ascent, descent, x_height, cap_height)


def get_name_strings(width_mode):
    display_name = f'{display_name_prefix} {width_mode}'
    unique_name = f'{unique_name_prefix}-{width_mode}-{style_name}'
    return {
        'copyright': copyright_string,
        'familyName': display_name,
        'styleName': style_name,
        'uniqueFontIdentifier': f'{unique_name};{version}',
        'fullName': display_name,
        'version': version,
        'psName': unique_name,
        'designer': designer,
        'description': description,
        'vendorURL': vendor_url,
        'designerURL': designer_url,
        'licenseDescription': license_description,
        'licenseInfoURL': license_info_url,
    }


def get_font_file_name(width_mode, font_format):
    return f'{output_name_prefix}-{width_mode}.{font_format}'


def get_info_file_name(width_mode):
    return f'font-info-{width_mode}.md'


def get_alphabet_txt_file_name(width_mode):
    return f'alphabet-{width_mode}.txt'


def get_release_zip_file_name(width_mode, font_format):
    return f'{output_name_prefix}-font-{width_mode}-{font_format}-v{version}.zip'


def get_alphabet_html_file_name(width_mode):
    return f'alphabet-{width_mode}.html'
