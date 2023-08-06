# -*- coding: utf-8 -*-
from parsers import parse_token


def str_int_to_int():
    print(parse_token("$int(42)"))


def str_float_to_float():
    print(parse_token("$float(42.7)"))


def rnd_int_between():
    print(parse_token("$int(5, 42)"))


def rnd_float_between():
    print(parse_token("$float(5, 42)"))


def rnd_choice_int():
    print(parse_token("$int(1,2,3,4,5,6,7,8)"))


def rnd_choice_float():
    print(parse_token("$float(1,2,3,4,5,6,7,8)"))


if __name__ == '__main__':
    str_int_to_int()
    str_float_to_float()
    rnd_int_between()
    rnd_float_between()
    rnd_choice_int()
    rnd_choice_float()
