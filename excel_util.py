# encoding: utf-8
# file:
# author: wu ming ming

import os
import re
from openpyxl import worksheet, load_workbook
from openpyxl.utils import cell
from collections import OrderedDict
# from ConfigParser import ConfigParser


def str2unicode(string):
    if not isinstance(string, unicode):
        return string.encode('utf-8')
    else:
        return string


def create_pattern_from_sting(string):
    if not isinstance(string, str):
        raise TypeError

    tags = re.findall('\W', string)
    pattern = '(.*'
    for tag in tags:
        pattern += tag + '.*'
    pattern += ')'
    return pattern, re.compile(pattern)


class EXCEL(object):
    '''excel driver'''

    def __init__(self, file_path):
        if not os.path.exists(file_path):
            raise ValueError
        self.file_path = file_path
        try:
            self.workbook = load_workbook(self.file_path, data_only=True)
        except IOError:
            raise IOError

    def get_sheets_by_name(self, name_list):
        if not isinstance(name_list, list):
            raise TypeError
        sheets = []
        for name in name_list:
            for sheet in self.workbook:
                if name in sheet.title:
                    sheets.append(sheet)
        return sheets

    def coordinate_in_region(self, coordinate, region_start, region_end):
        '''判断单元格是否在区间内'''
        if not isinstance(coordinate, str) or not isinstance(region_start, str) or not isinstance(region_end, str):
            raise TypeError
        try:
            co = cell.coordinate_from_string(coordinate)
            co_re_s = cell.coordinate_from_string(region_start)
            co_re_e = cell.coordinate_from_string(region_end)
            if co[0] in cell.get_column_interval(co_re_s[0], co_re_e) and co[1] in range(co_re_s[1], co_re_e[1]+1):
                return True
            else:
                return False
        except:
            raise ValueError

    def is_merged_cell(self, sheet, coordinate):
        '''单元格是否在合并单元格内'''
        if not isinstance(sheet, worksheet) or not isinstance(coordinate, str):
            raise TypeError
        return coordinate in sheet.merged_cells

    def get_merged_region(self, sheet, coordinate):
        '''返回单元格所在的合并单元格'''
        if not isinstance(sheet, worksheet):
            raise TypeError
        for region in sheet.merged_cell_ranges:
            re_co = region.split(':')
            if self.coordinate_in_region(coordinate, re_co[0], re_co[1]):
                return region
        return None

    def get_merged_value(self, sheet, region):
        '''返回合并单元格的值'''
        if not isinstance(sheet, worksheet):
            raise TypeError
        try:
            re_co = region.split(':')
            region_x = self.get_merged_region(sheet, re_co[0])
            region_y = self.get_merged_region(sheet, re_co[1])
            if region_x == region_y:
                return sheet[region_x.split(':')[0]].value
            else:
                return None
        except:
            raise

    def get_coordinates_value(self, sheet, cfg_list, start_row=None, end_row=None, offset=None):
        '''以字典方式返回多区域单元格的值
        :param
        sheet: worksheet
        args[0]:
        [
            {
                'column': # 'A'
                'pattern': # '(\w\d{2}/\d{2}(?#D12/34))'
                'key_name': # 'name'
                'start_row': # 10
                'end_row': # 20
                'sub_keys':[
                    {
                        'column': # 'B'
                        'pattern': # '(\w\d{2}/\d{2}(?#D12/34))'
                        'key_name': # 'server_typ'
                        'start_row': # 10
                        'end_row': # 20
                        'sub_keys':[
                            {
                                ...
                            }
                    }
                    ...
                ]
            },
            ...
        ]
        args[1]: start_row
        args[2]: end_row
        args[3]: offset # 外层调用不传offset

        :return
        {
            'name':{
                'server_type':{
                    ... # value or dict
                }
                '...'
            }
            ...
        }
        '''

        if not isinstance(sheet, worksheet):
            raise TypeError
        if not isinstance(cfg_list, list):
            raise TypeError
        if offset and not isinstance(offset, int):
            raise TypeError
        if start_row and not isinstance(start_row, int):
            raise TypeError
        if end_row and not isinstance(end_row, int):
            raise TypeError

        co_value_dict = OrderedDict()

        for cfg in cfg_list:
            if not isinstance(cfg, dict):
                raise TypeError

            # 内层参数优先于外层参数，
            if 'start_row' in cfg.keys() and 'end_row' in cfg.keys() and isinstance(cfg['start_row'], int) and isinstance(cfg['end_row']):
                _start_row = cfg['start_row']
                _end_row = cfg['end_row']
            elif start_row and end_row:
                _start_row = start_row
                _end_row = end_row
            else:
                _start_row = 1
                _end_row = sheet.rows
            if offset:
                _start_row = _start_row + offset
                _end_row = start_row + 1

            try:
                for row in range(_start_row, _end_row + 1):
                    # 获取单元格值
                    coordinate = cfg['column'] + str(row)
                    if self.is_merged_cell(coordinate):
                        value = sheet[self.get_merged_region(sheet, coordinate).split(':')[0]]
                        if 'keys' in cfg.keys():
                            import warnings
                            warnings.warn('{0}{1} is merged cell, should not had keys config ...')
                    else:
                        value = sheet[coordinate]

                    # 判断有效性
                    if value:
                        # 未匹配正则
                        if 'pattern' in cfg and cfg['pattern'] and re.match(cfg['pattern'], value) is None:
                            # 递归调用才传offset，外层调用不传offset
                            if offset:
                                value = coordinate + '_match_failed'
                            else:
                                # 首列不匹配跳过
                                continue
                    elif offset:
                        # 递归调用时空值
                        value = coordinate + '_is_none'
                    else:
                        # 首列空值跳过
                        continue

                    # 递归调用查找字典各值
                    if 'keys' in cfg.keys():
                        co_value_dict [value] = OrderedDict()
                        sub_value = self.get_coordinates_value(sheet, cfg['keys'], row, row, row - _start_row)
                        for s_key, s_value in sub_value.items():
                            co_value_dict[value][s_key] = s_value
                    else:
                        co_value_dict[cfg['key_name']] = value
            except:
                raise

            return co_value_dict


if __name__ == '__main__':
    pattern, _ = create_pattern_from_sting('asd/sfw/fea/wer-123')
    print pattern
    print re.match(pattern, 'asd/sfw/fea/wer-123').string

    pass
