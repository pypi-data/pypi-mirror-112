# -*- coding: utf-8 -*-
from parsers import parse_token


def generate_unique_guid():
    guids = []
    for i in range(1000):
        guids.append(parse_token("$guid(true)"))

    print(f"Generated guid: {set(guids)}")


def generate_random_guids():
    guids = []
    for i in range(15):
        guids.append(parse_token("$guid()"))

    print(f"Generated guids: {set(guids)}")


if __name__ == '__main__':
    generate_unique_guid()
    generate_random_guids()