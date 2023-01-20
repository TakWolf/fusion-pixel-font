import logging
import os

import minify_html
from PIL import ImageFont, Image, ImageDraw

import configs
from configs import path_define
from utils import unidata_util, gb2312_util, big5_util, shift_jis_util, ks_x_1001_util

logger = logging.getLogger('info-service')


def _get_unicode_char_count_infos(alphabet):
    count_map = {}
    for c in alphabet:
        code_point = ord(c)
        unicode_block = configs.unidata_db.get_block_by_code_point(code_point)
        if not c.isprintable() and unicode_block.char_count > 0:
            continue
        count = count_map.get(unicode_block.begin, 0)
        count += 1
        count_map[unicode_block.begin] = count
    begins = list(count_map.keys())
    begins.sort()
    return [(configs.unidata_db.get_block_by_code_point(begin), count_map[begin]) for begin in begins]


def _get_locale_char_count_map(alphabet, query_block_func):
    count_map = {}
    for c in alphabet:
        block_name = query_block_func(c)
        if block_name:
            block_count = count_map.get(block_name, 0)
            block_count += 1
            count_map[block_name] = block_count
            total_count = count_map.get('total', 0)
            total_count += 1
            count_map['total'] = total_count
    return count_map


def _get_gb2312_char_count_infos(alphabet):
    count_map = _get_locale_char_count_map(alphabet, gb2312_util.query_block)
    return [
        ('一级汉字', count_map.get('level-1', 0), gb2312_util.alphabet_level_1_count),
        ('二级汉字', count_map.get('level-2', 0), gb2312_util.alphabet_level_2_count),
        ('其他字符', count_map.get('other', 0), gb2312_util.alphabet_other_count),
        ('总计', count_map.get('total', 0), gb2312_util.alphabet_count),
    ]


def _get_big5_char_count_infos(alphabet):
    count_map = _get_locale_char_count_map(alphabet, big5_util.query_block)
    return [
        ('常用汉字', count_map.get('level-1', 0), big5_util.alphabet_level_1_count),
        ('次常用汉字', count_map.get('level-2', 0), big5_util.alphabet_level_2_count),
        ('其他字符', count_map.get('other', 0), big5_util.alphabet_other_count),
        ('总计', count_map.get('total', 0), big5_util.alphabet_count),
    ]


def _get_shift_jis_char_count_infos(alphabet):
    count_map = _get_locale_char_count_map(alphabet, shift_jis_util.query_block)
    return [
        ('单字节-ASCII字符', count_map.get('single-ascii', 0), shift_jis_util.alphabet_single_ascii_count),
        ('单字节-半角标点和片假名', count_map.get('single-other', 0), shift_jis_util.alphabet_single_other_count),
        ('双字节-假名和其他字符', count_map.get('double-basic', 0), shift_jis_util.alphabet_double_basic_count),
        ('双字节-汉字', count_map.get('double-word', 0), shift_jis_util.alphabet_double_word_count),
        ('总计', count_map.get('total', 0), shift_jis_util.alphabet_count),
    ]


def _get_ks_x_1001_char_count_infos(alphabet):
    count_map = _get_locale_char_count_map(alphabet, ks_x_1001_util.query_block)
    return [
        ('谚文音节', count_map.get('syllable', 0), ks_x_1001_util.alphabet_syllable_count),
        ('汉字', count_map.get('word', 0), ks_x_1001_util.alphabet_word_count),
        ('其他字符', count_map.get('other', 0), ks_x_1001_util.alphabet_other_count),
        ('总计', count_map.get('total', 0), ks_x_1001_util.alphabet_count),
    ]


def _write_unicode_char_count_infos_table(file, infos):
    file.write('| 区块范围 | 区块名称 | 区块含义 | 覆盖数 | 覆盖率 |\n')
    file.write('|---|---|---|---:|---:|\n')
    for unicode_block, count in infos:
        code_point_range = f'{unicode_block.begin:04X} ~ {unicode_block.end:04X}'
        if unicode_block.char_count > 0:
            progress = count / unicode_block.char_count
        else:
            progress = 1
        finished_emoji = '🚩' if progress == 1 else '🚧'
        file.write(f'| {code_point_range} | {unicode_block.name} | {unicode_block.name_cn if unicode_block.name_cn else ""} | {count} / {unicode_block.char_count} | {progress:.2%} {finished_emoji} |\n')


def _write_locale_char_count_infos_table(file, infos):
    file.write('| 区块名称 | 覆盖数 | 覆盖率 |\n')
    file.write('|---|---:|---:|\n')
    for title, count, total in infos:
        progress = count / total
        finished_emoji = '🚩' if progress == 1 else '🚧'
        file.write(f'| {title} | {count} / {total} | {progress:.2%} {finished_emoji} |\n')


def make_info_file(alphabet):
    file_output_path = os.path.join(path_define.outputs_dir, 'font-info.md')
    with open(file_output_path, 'w', encoding='utf-8') as file:
        file.write('# 缝合怪像素字体 / Fusion Pixel Font\n')
        file.write('\n')
        file.write('## 基本信息\n')
        file.write('\n')
        file.write('| 属性 | 值 |\n')
        file.write('|---|---|\n')
        file.write(f'| 字符总数 | {len(alphabet)} |\n')
        file.write('\n')
        file.write('## Unicode 字符分布\n')
        file.write('\n')
        file.write(f'区块定义参考：[{unidata_util.blocks_doc_url}]({unidata_util.blocks_doc_url})\n')
        file.write('\n')
        _write_unicode_char_count_infos_table(file, _get_unicode_char_count_infos(alphabet))
        file.write('\n')
        file.write('## GB2312 字符分布\n')
        file.write('\n')
        file.write('简体中文参考字符集。统计范围不包含 ASCII。\n')
        file.write('\n')
        _write_locale_char_count_infos_table(file, _get_gb2312_char_count_infos(alphabet))
        file.write('\n')
        file.write('## Big5 字符分布\n')
        file.write('\n')
        file.write('繁体中文参考字符集。统计范围不包含 ASCII。\n')
        file.write('\n')
        _write_locale_char_count_infos_table(file, _get_big5_char_count_infos(alphabet))
        file.write('\n')
        file.write('## Shift-JIS 字符分布\n')
        file.write('\n')
        file.write('日语参考字符集。\n')
        file.write('\n')
        _write_locale_char_count_infos_table(file, _get_shift_jis_char_count_infos(alphabet))
        file.write('\n')
        file.write('## KS X 1001 字符分布\n')
        file.write('\n')
        file.write('韩语参考字符集。统计范围不包含 ASCII。\n')
        file.write('\n')
        _write_locale_char_count_infos_table(file, _get_ks_x_1001_char_count_infos(alphabet))
    logger.info(f'make {file_output_path}')


def make_preview_image_file():
    px = configs.font_config[0]
    image_font = ImageFont.truetype(os.path.join(path_define.outputs_dir, 'fusion-pixel.otf'), px)
    image = Image.new('RGBA', (px * 35, px * 19), (255, 255, 255))
    ImageDraw.Draw(image).text((px, px), '缝合怪像素字体 / Fusion Pixel Font', fill=(0, 0, 0), font=image_font)
    ImageDraw.Draw(image).text((px, px * 3), '我们每天度过的称之为日常的生活，其实是一个个奇迹的连续也说不定。', fill=(0, 0, 0), font=image_font)
    ImageDraw.Draw(image).text((px, px * 5), '我們每天度過的稱之為日常的生活，其實是一個個奇跡的連續也說不定。', fill=(0, 0, 0), font=image_font)
    ImageDraw.Draw(image).text((px, px * 7), '日々、私たちが過ごしている日常は、実は奇跡の連続なのかもしれない。', fill=(0, 0, 0), font=image_font)
    ImageDraw.Draw(image).text((px, px * 9), 'THE QUICK BROWN FOX JUMPS OVER A LAZY DOG.', fill=(0, 0, 0), font=image_font)
    ImageDraw.Draw(image).text((px, px * 11), 'the quick brown fox jumps over a lazy dog.', fill=(0, 0, 0), font=image_font)
    ImageDraw.Draw(image).text((px, px * 13), '0123456789', fill=(0, 0, 0), font=image_font)
    ImageDraw.Draw(image).text((px, px * 15), '★☆☺☹♠♡♢♣♤♥♦♧☀☼♩♪♫♬☂☁⚓✈⚔☯', fill=(0, 0, 0), font=image_font)
    ImageDraw.Draw(image).text((px, px * 17), '☜☝☞☟♔♕♖♗♘♙♚♛♜♝♞♟', fill=(0, 0, 0), font=image_font)
    image = image.resize((image.width * 2, image.height * 2), Image.NEAREST)
    file_output_path = os.path.join(path_define.outputs_dir, 'preview.png')
    image.save(file_output_path)
    logger.info(f'make {file_output_path}')


def make_alphabet_txt_file(alphabet):
    file_output_path = os.path.join(path_define.outputs_dir, 'alphabet.txt')
    with open(file_output_path, 'w', encoding='utf-8') as file:
        file.write(''.join(alphabet))
    logger.info(f'make {file_output_path}')


def make_alphabet_html_file(alphabet):
    template = configs.template_env.get_template('alphabet.html')
    html = template.render(alphabet=''.join([c for c in alphabet if ord(c) >= 128]))
    html = minify_html.minify(html, minify_css=True, minify_js=True)
    file_output_path = os.path.join(path_define.outputs_dir, 'alphabet.html')
    with open(file_output_path, 'w', encoding='utf-8') as file:
        file.write(html)
    logger.info(f'make {file_output_path}')
