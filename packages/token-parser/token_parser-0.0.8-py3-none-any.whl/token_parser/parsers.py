# -*- coding: utf-8 -*-
import ast
from datetime import datetime, timedelta
import random
import pytz
from dateutil.parser import parse
import json
from dateutil.relativedelta import relativedelta
from uuid import uuid4


ISO8601_DATE_FORMAT_UTC = "%Y-%m-%dT%H:%M:%S.%fZ"
ISO8601_DATE_FORMAT_LOCAL = ISO8601_DATE_FORMAT_UTC[:-1]
CURRENT_INC_VALUE = 0
DEFAULT_INC_BY_VALUE = 1
CURRENT_DEC_VALUE = 0
DEFAULT_DEC_BY_VALUE = 1
CURRENT_GUID = None
NEXT_MAP = {}


def _get_now_(now_ref, is_utc: bool):
    if now_ref is None:
        return datetime.now() if not is_utc else datetime.utcnow().astimezone(pytz.utc)

    return now_ref if not is_utc else now_ref.astimezone(pytz.utc)


def _get_number_(required, num_type):
    req_num_size = len(required)

    if req_num_size == 0:
        return 0

    if req_num_size == 1:
        return num_type(required[0])

    if req_num_size == 2:
        if num_type == float:
            return random.uniform(num_type(required[0]), num_type(required[1]))
        else:
            return random.randint(num_type(required[0]), num_type(required[1]))

    return random.choice([num_type(n) for n in required])


def _get_int_(text) -> int:
    required_numbers = text.replace("$int(", "")[:-1].split(",")
    return _get_number_(required_numbers, int)


def _get_float_(text) -> float:
    required_numbers = text.replace("$float(", "")[:-1].split(",")
    return _get_number_(required_numbers, float)


def _prepare_base_date_(dt_text, dt_ref, is_utc):
    if dt_ref is not None:
        return dt_ref

    if dt_text == "now":
        return datetime.now()

    elif dt_text == "utcNow":
        return datetime.utcnow().astimezone(pytz.utc)

    try:
        dt = datetime.strptime(dt_text, ISO8601_DATE_FORMAT_UTC)
        if is_utc:
            dt = dt.replace(tzinfo=pytz.utc)
        return dt

    except ValueError:
        return parse(dt_text)


def _parse_options_json_(options_txt) -> dict:
    try:
        return json.loads(options_txt)
    except (TypeError, ValueError):
        return ast.literal_eval(options_txt)


def _get_date_added_(dt_text, options_txt, dt_ref: datetime = None):
    base_dt = _prepare_base_date_(dt_text, dt_ref, is_utc=dt_text.upper().endswith("Z"))
    options = _parse_options_json_(options_txt) if len(options_txt) > 0 else {}

    for op_key in ["microseconds", "milliseconds", "seconds", "minutes", "hours", "days", "weeks", "months", "years"]:
        val = options.get(op_key)
        if val is None:
            continue

        if op_key in ["months", "years"]:
            base_dt += relativedelta(**{op_key: val})
        else:
            base_dt += timedelta(**{op_key: val})

    return base_dt


def _get_inc_by_(text: str) -> int:
    global CURRENT_INC_VALUE
    global DEFAULT_INC_BY_VALUE

    inc_by_str = text.replace("$inc(", "")[:-1].strip()
    CURRENT_INC_VALUE += DEFAULT_INC_BY_VALUE if inc_by_str == "" else int(inc_by_str)
    return CURRENT_INC_VALUE


def _reset_inc_by_() -> None:
    global CURRENT_INC_VALUE
    CURRENT_INC_VALUE = 0


def _get_dec_by_(text: str) -> int:
    global CURRENT_DEC_VALUE
    global DEFAULT_DEC_BY_VALUE

    inc_by_str = text.replace("$dec(", "")[:-1].strip()
    CURRENT_DEC_VALUE -= DEFAULT_DEC_BY_VALUE if inc_by_str == "" else int(inc_by_str)
    return CURRENT_DEC_VALUE


def _reset_dec_by_() -> None:
    global CURRENT_DEC_VALUE
    CURRENT_DEC_VALUE = 0


def _extract_date_add_params_(date_add):
    params = [s.strip() for s in date_add.split(",")]
    if len(params) > 2:
        params = [
            params[0],
            ", ".join(params[1:])
        ]
    return params


def _get_guid_(text):
    global CURRENT_GUID

    keep_str = text.replace("$guid(", "")[:-1].strip()
    keep = keep_str.upper() == "TRUE"
    if keep and CURRENT_GUID is None:
        CURRENT_GUID = str(uuid4())

    return CURRENT_GUID if keep else str(uuid4())


def _get_next_(text):
    global NEXT_MAP
    list_str = text.replace("$next(", "")[:-1].strip()
    if len(list_str) == 0:
        return text

    if NEXT_MAP.get(list_str) is None:
        try:
            parsed_list = ast.literal_eval(list_str)
        except SyntaxError:
            return text

        if len(parsed_list) == 0:
            return text

        NEXT_MAP[list_str] = {
            "parsed": parsed_list,
            "iter": iter(parsed_list)
        }

    try:
        return next(NEXT_MAP[list_str]["iter"])
    except StopIteration:
        if len(NEXT_MAP[list_str]["parsed"]) == 0:
            return text

        NEXT_MAP[list_str]["iter"] = iter(NEXT_MAP[list_str]["parsed"])
        return next(NEXT_MAP[list_str]["iter"])


def parse_token(text: str) -> any:
    if not isinstance(text, str) or text is None or text.strip() == "":
        return None

    _text = text.strip()

    if _text in ["$now()", "$utcNow()"]:
        is_utc = _text == "$utcNow()"
        return _get_now_(now_ref=None, is_utc=is_utc)

    if not _text.endswith(")"):
        return text

    if any(x in _text for x in ["$now(", "$utcNow("]):
        is_utc = _text.startswith("$utcNow")
        dt_text = _text.replace("$utcNow(", "").replace("$now(", "")
        return _get_now_(
            now_ref=_prepare_base_date_(
                dt_text=dt_text[:len(dt_text) - 1], dt_ref=None, is_utc=is_utc
            ),
            is_utc=is_utc
        )

    if _text.startswith("$int("):
        return _get_int_(_text)

    if _text.startswith("$float("):
        return _get_float_(_text)

    if _text.startswith("$inc("):
        return _get_inc_by_(_text)

    if _text.startswith("$incReset("):
        _reset_inc_by_()
        return True

    if _text.startswith("$dec("):
        return _get_dec_by_(_text)

    if _text.startswith("$decReset("):
        _reset_dec_by_()
        return True

    if _text.startswith("$dateAdd("):
        date_add = _text.replace("$dateAdd(", "")
        date_add = date_add[:len(date_add) - 1]
        date_add_parts = _extract_date_add_params_(date_add)

        if len(date_add_parts) == 1:
            date_add_parts.append("{}")

        return _get_date_added_(*date_add_parts)

    if _text.startswith("$guid("):
        return _get_guid_(_text)

    if _text.startswith("$next("):
        return _get_next_(_text)

    return text


if __name__ == '__main__':
    now = datetime.now()
    now_str = now.strftime(ISO8601_DATE_FORMAT_UTC)
    parsed_token = parse_token(f"$now({now_str})")
    print(parsed_token)
