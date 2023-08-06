# -*- coding: utf-8 -*-
from datetime import datetime
import pytz

from parsers import parse_token

ISO8601_DATE_FORMAT_UTC = "%Y-%m-%dT%H:%M:%S.%fZ"
ISO8601_DATE_FORMAT_LOCAL = ISO8601_DATE_FORMAT_UTC[:-1]


def adding_two_days_to_local_datetime():
    now = datetime.now()
    now_str = now.strftime(ISO8601_DATE_FORMAT_LOCAL)
    options = str({
        "days": 2
    })
    adjusted_date = parse_token(f"$dateAdd({now_str}, {options})")
    print(f"Date '{now_str}' +2 days == {adjusted_date}")


def adding_two_days_to_utc_datetime():
    now = datetime.utcnow().astimezone(pytz.utc)
    now_str = now.strftime(ISO8601_DATE_FORMAT_UTC)
    options = str({
        "days": 2
    })
    adjusted_date = parse_token(f"$dateAdd({now_str}, {options})")
    print(f"Date (UTC) '{now_str}' +2 days == {adjusted_date}")


def adding_multi_part_to_local_datetime():
    now = datetime.now()
    now_str = now.strftime(ISO8601_DATE_FORMAT_LOCAL)
    options = str({
        "days": 2,
        "hours": 12,
        "minutes": 17
    })

    adjusted_date = parse_token(f"$dateAdd({now_str}, {options})")
    print(f"Date '{now_str}' +2 days, 12 hours and 17 minutes == {adjusted_date}")


def adding_multi_part_to_utc_datetime():
    now = datetime.utcnow().astimezone(pytz.utc)
    now_str = now.strftime(ISO8601_DATE_FORMAT_UTC)
    options = str({
        "days": 2,
        "hours": 12,
        "minutes": 17
    })

    adjusted_date = parse_token(f"$dateAdd({now_str}, {options})")
    print(f"Date (UTC) '{now_str}' +2 days, 12 hours and 17 minutes == {adjusted_date}")


if __name__ == '__main__':
    adding_two_days_to_local_datetime()
    adding_two_days_to_utc_datetime()
    adding_multi_part_to_local_datetime()
    adding_multi_part_to_utc_datetime()
