import re


def find_all_index(pattern, string, flags=0):
    """find all matched index of string"""
    return [i.span() for i in re.finditer(pattern, string, flags=flags)]


def string_add(string: str, dx=1):
    # count_points = string.count('.')
    items = find_all_index(r"\.", string)
    number_list = [i for i in string.split('.')]
    number_str = "".join(number_list)
    number_len = len(number_str)
    number = int(number_str)
    number += dx
    new_number_str = f"{number:0>{number_len}d}"
    new_number_list = list(new_number_str)
    [new_number_list.insert(idx[0], ".") for idx in items]
    return "".join(new_number_list)
