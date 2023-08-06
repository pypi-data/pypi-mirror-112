# -*- coding: utf-8 -*-
from parsers import parse_token


def inc_by_default():
    print("reset current counter")
    parse_token("$incReset()")

    print("getting incremental int, starting from one...")
    for i in range(10):
        print(parse_token("$inc()"))


def inc_by_n():
    print("reset current counter")
    parse_token("$incReset()")

    n = 3
    print(f"getting incremental (by {n}) int, starting from {n}...")
    for i in range(10):
        print(parse_token(f"$inc({n})"))


def dec_by_default():
    print("reset current counter")
    parse_token("$incReset()")

    print("getting decrementing int, starting from one...")
    for i in range(10):
        print(parse_token("$dec()"))


def dec_by_n():
    print("reset current counter")
    parse_token("$decReset()")

    n = 3
    print(f"getting decremental (by {n}) int, starting from -{n}...")
    for i in range(10):
        print(parse_token(f"$dec({n})"))


if __name__ == '__main__':
    inc_by_default()
    inc_by_n()
    dec_by_default()
    dec_by_n()
