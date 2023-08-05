import re
from re import compile


def findAllWithRe(data, pattern, dotAll=False):
    if dotAll:
        return compile(pattern, re.S).findall(data)
    else:
        return compile(pattern).findall(data)
