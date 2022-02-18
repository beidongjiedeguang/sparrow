import re
import cn2an


def find_all_index(pattern, string, flags=0):
    """find all matched index of string"""
    return [i.span() for i in re.finditer(pattern, string, flags=flags)]


def string_add(string: str, dx=1):
    # count_points = string.count('.')
    items = find_all_index(r"\.", string)
    number_list = [i for i in string.split(".")]
    number_str = "".join(number_list)
    number_len = len(number_str)
    number = int(number_str)
    number += dx
    new_number_str = f"{number:0>{number_len}d}"
    new_number_list = list(new_number_str)
    [new_number_list.insert(idx[0], ".") for idx in items]
    return "".join(new_number_list)


def index_char(L=1000):
    """
    Get the index of all characters.
    use chr()
    """
    index_token = {}
    token = []
    for i in range(L):
        character = chr(i)
        index_token[i] = character
        token.append(character)
    token_index = dict(zip(token, range(L)))  # token_index[idx] equal to ord(idx)
    return index_token, token_index


def find_match(start, end, S, flag=0):
    """find the string between `start` and `end` of `S`
    flag=0 defaults, means no special specification
    flag options:
        re.I    IGNORECASE， 忽略大小写的匹配模式
        re.M    MULTILINE，多行模式, 改变 ^ 和 $ 的行为
        re.S  　DOTALL，此模式下 '.' 的匹配不受限制，可匹配任何字符，包括换行符，也就是默认是不能匹配换行符
        re.X    VERBOSE，冗余模式， 此模式忽略正则表达式中的空白和#号的注释
    """
    try:
        START = re.search(start, S, flags=flag).span()[1]
        END = re.search(end, S, flags=flag).span()[0]
        return S[START:END]
    except:
        print("Do not match anything.")
        return None


def find_match2(pattern, S, flag=0):
    res = re.search(pattern, S, flags=flag)
    return res.group()
