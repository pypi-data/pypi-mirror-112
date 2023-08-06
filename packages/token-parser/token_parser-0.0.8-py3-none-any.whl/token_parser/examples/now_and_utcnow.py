# -*- coding: utf-8 -*-
from parsers import parse_token


def get_current_datetime():
    now = parse_token("$now()")
    print(f"Current time: {now}")


def get_specific_datetime_string_to_object():
    date = "2021-06-30T12:00:00.000"
    now = parse_token(f"$now({date})")
    print(f"String '{date}' converted to datetime: {now}")


def get_utc_current_datetime():
    now = parse_token("$utcNow()")
    print(f"Current time in UTC: {now}")


def get_specific_utc_datetime_string_to_object():
    date = "2021-06-30T12:00:00.000Z"
    now = parse_token(f"$utcNow({date})")
    print(f"String '{date}' converted to UTC datetime: {now}")


if __name__ == '__main__':
    get_current_datetime()
    get_specific_datetime_string_to_object()
    get_utc_current_datetime()
    get_specific_utc_datetime_string_to_object()
