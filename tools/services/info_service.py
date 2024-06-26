import logging
from collections import defaultdict
from collections.abc import Callable
from io import StringIO
from typing import TextIO

import unidata_blocks
from character_encoding_utils import gb2312, big5, shiftjis, ksx1001
from unidata_blocks import UnicodeBlock

from tools import configs
from tools.configs import path_define
from tools.services.font_service import DesignContext

logger = logging.getLogger(__name__)


def _get_unicode_chr_count_infos(alphabet: set[str]) -> list[tuple[UnicodeBlock, int]]:
    count_infos = defaultdict(int)
    for c in alphabet:
        code_point = ord(c)
        block = unidata_blocks.get_block_by_code_point(code_point)
        if not c.isprintable() and block.printable_count > 0:
            continue
        count_infos[block.code_start] += 1
    return [(unidata_blocks.get_block_by_code_point(code_start), count) for code_start, count in sorted(count_infos.items())]


def _get_locale_chr_count_infos(alphabet: set[str], query_category_func: Callable[[str], str | None]) -> defaultdict[str, int]:
    count_infos = defaultdict(int)
    for c in alphabet:
        category = query_category_func(c)
        if category is not None:
            count_infos[category] += 1
            count_infos['total'] += 1
    return count_infos


def _get_gb2312_chr_count_infos(alphabet: set[str]) -> list[tuple[str, int, int]]:
    count_infos = _get_locale_chr_count_infos(alphabet, gb2312.query_category)
    return [
        ('一级汉字', count_infos['level-1'], gb2312.get_level_1_count()),
        ('二级汉字', count_infos['level-2'], gb2312.get_level_2_count()),
        ('其他字符', count_infos['other'], gb2312.get_other_count()),
        ('总计', count_infos['total'], gb2312.get_count()),
    ]


def _get_big5_chr_count_infos(alphabet: set[str]) -> list[tuple[str, int, int]]:
    count_infos = _get_locale_chr_count_infos(alphabet, big5.query_category)
    return [
        ('常用汉字', count_infos['level-1'], big5.get_level_1_count()),
        ('次常用汉字', count_infos['level-2'], big5.get_level_2_count()),
        ('其他字符', count_infos['other'], big5.get_other_count()),
        ('总计', count_infos['total'], big5.get_count()),
    ]


def _get_shiftjis_chr_count_infos(alphabet: set[str]) -> list[tuple[str, int, int]]:
    count_infos = _get_locale_chr_count_infos(alphabet, shiftjis.query_category)
    return [
        ('单字节-ASCII可打印字符', count_infos['single-byte-ascii-printable'], shiftjis.get_single_byte_ascii_printable_count()),
        ('单字节-半角片假名', count_infos['single-byte-half-width-katakana'], shiftjis.get_single_byte_half_width_katakana_count()),
        ('双字节-其他字符', count_infos['double-byte-other'], shiftjis.get_double_byte_other_count()),
        ('双字节-汉字', count_infos['double-byte-kanji'], shiftjis.get_double_byte_kanji_count()),
        ('总计', count_infos['total'] - count_infos['single-byte-ascii-control'], shiftjis.get_count() - shiftjis.get_single_byte_ascii_control_count()),
    ]


def _get_ksx1001_chr_count_infos(alphabet: set[str]) -> list[tuple[str, int, int]]:
    count_infos = _get_locale_chr_count_infos(alphabet, ksx1001.query_category)
    return [
        ('谚文音节', count_infos['syllable'], ksx1001.get_syllable_count()),
        ('汉字', count_infos['hanja'], ksx1001.get_hanja_count()),
        ('其他字符', count_infos['other'], ksx1001.get_other_count()),
        ('总计', count_infos['total'], ksx1001.get_count()),
    ]


def _write_unicode_chr_count_infos_table(output: TextIO, infos: list[tuple[UnicodeBlock, int]]):
    output.write('| 区块范围 | 区块名称 | 区块含义 | 完成数 | 缺失数 | 进度 |\n')
    output.write('|---|---|---|---:|---:|---:|\n')
    for block, count in infos:
        code_point_range = f'{block.code_start:04X} ~ {block.code_end:04X}'
        name = block.name
        name_zh = block.name_localized('zh', '')
        total = block.printable_count
        missing = total - count if total > 0 else 0
        progress = count / total if total > 0 else 1
        finished_emoji = '🚩' if progress == 1 else '🚧'
        output.write(f'| {code_point_range} | {name} | {name_zh} | {count} / {total} | {missing} | {progress:.2%} {finished_emoji} |\n')


def _write_locale_chr_count_infos_table(output: TextIO, infos: list[tuple[str, int, int]]):
    output.write('| 区块名称 | 完成数 | 缺失数 | 进度 |\n')
    output.write('|---|---:|---:|---:|\n')
    for name, count, total in infos:
        missing = total - count
        progress = count / total
        finished_emoji = '🚩' if progress == 1 else '🚧'
        output.write(f'| {name} | {count} / {total} | {missing} | {progress:.2%} {finished_emoji} |\n')


def make_font_info(design_context: DesignContext, width_mode: str):
    alphabet = design_context.get_alphabet(width_mode)

    output = StringIO()
    output.write(f'# Fusion Pixel {design_context.font_config.font_size}px {'等宽模式' if width_mode == 'monospaced' else '比例模式'}\n')
    output.write('\n')
    output.write('## 基本信息\n')
    output.write('\n')
    output.write('| 属性 | 值 |\n')
    output.write('|---|---|\n')
    output.write(f'| 版本号 | {configs.font_version} |\n')
    output.write(f'| 字符总数 | {len(alphabet)} |\n')
    output.write('\n')
    output.write('## Unicode 字符分布\n')
    output.write('\n')
    output.write(f'Unicode 版本：{unidata_blocks.unicode_version}\n')
    output.write('\n')
    _write_unicode_chr_count_infos_table(output, _get_unicode_chr_count_infos(alphabet))
    output.write('\n')
    output.write('## GB2312 字符分布\n')
    output.write('\n')
    output.write('简体中文参考字符集。统计范围不包含 ASCII。\n')
    output.write('\n')
    _write_locale_chr_count_infos_table(output, _get_gb2312_chr_count_infos(alphabet))
    output.write('\n')
    output.write('## Big5 字符分布\n')
    output.write('\n')
    output.write('繁体中文参考字符集。统计范围不包含 ASCII。\n')
    output.write('\n')
    _write_locale_chr_count_infos_table(output, _get_big5_chr_count_infos(alphabet))
    output.write('\n')
    output.write('## Shift-JIS 字符分布\n')
    output.write('\n')
    output.write('日语参考字符集。\n')
    output.write('\n')
    _write_locale_chr_count_infos_table(output, _get_shiftjis_chr_count_infos(alphabet))
    output.write('\n')
    output.write('## KS-X-1001 字符分布\n')
    output.write('\n')
    output.write('韩语参考字符集。统计范围不包含 ASCII。\n')
    output.write('\n')
    _write_locale_chr_count_infos_table(output, _get_ksx1001_chr_count_infos(alphabet))

    path_define.outputs_dir.mkdir(parents=True, exist_ok=True)
    file_path = path_define.outputs_dir.joinpath(f'font-info-{design_context.font_config.font_size}px-{width_mode}.md')
    file_path.write_text(output.getvalue(), 'utf-8')
    logger.info("Make font info: '%s'", file_path)


def make_alphabet_txt(design_context: DesignContext, width_mode: str):
    alphabet = sorted(design_context.get_alphabet(width_mode))

    path_define.outputs_dir.mkdir(parents=True, exist_ok=True)
    file_path = path_define.outputs_dir.joinpath(f'alphabet-{design_context.font_config.font_size}px-{width_mode}.txt')
    file_path.write_text(''.join(alphabet), 'utf-8')
    logger.info("Make alphabet txt: '%s'", file_path)
