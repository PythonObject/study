# encoding: utf-8
# file name: 
__author__ = 'wu ming ming'

import re
from collections import OrderedDict

def sorted_dict_by_key_digit(dict_value):
    ''''''
    if not isinstance(dict_value, dict):
        raise TypeError
    value_tmp = dict_value.items()
    for count in range(len(re.findall('\d+', dict_value.keys()[0])))[::-1]:
        value_tmp = sorted(value_tmp, key=lambda x: int(re.findall('\d+', x[0])[count]))
    sorted_result = OrderedDict()
    for value in value_tmp:
        sorted_result[value[0]] = value[1]
    return sorted_result


if __name__ == '__main__':
    pass
    dict_value = {
        '12A/Frame12/1U23': {'a': 1},
        '14A/Frame10/1U20': {'a': 1},
        '15A/Frame1/1U12': {'a': 1},
        '13A/Frame8/1U25': {'a': 1},
        '10A/Frame23/1U43': {'a': 1},
        '12A/Frame10/1U23': {'a': 1},
        '14A/Frame13/1U20': {'a': 1},
        '15A/Frame40/1U12': {'a': 1},
        '13A/Frame12/1U25': {'a': 1},
        '10A/Frame7/1U43': {'a': 1},
        '12A/Frame10/2U23': {'a': 1},
        '14A/Frame13/4U20': {'a': 1},
        '15A/Frame40/5U12': {'a': 1},
        '13A/Frame12/3U25': {'a': 1},
        '10A/Frame7/9U43': {'a': 1},
    }

    print sorted_dict_by_key_digit(dict_value)
