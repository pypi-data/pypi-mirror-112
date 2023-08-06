# -*- coding: utf-8 -*-
import unittest
from datetime import datetime, timedelta
from uuid import UUID
from dateutil.relativedelta import relativedelta
import pytz
from parameterized import parameterized

from parsers import parse_token

ISO8601_DATE_FORMAT_UTC = "%Y-%m-%dT%H:%M:%S.%fZ"
ISO8601_DATE_FORMAT_LOCAL = ISO8601_DATE_FORMAT_UTC[:-1]
DATE_ADD_REPLACE_TEST_PARAMS = [
    ["microseconds", 0], ["microseconds", 100], ["microseconds", -100], ["microseconds", 77], ["microseconds", -77],
    ["milliseconds", 0], ["milliseconds", 100], ["milliseconds", -100], ["milliseconds", 77], ["milliseconds", -77],
    ["seconds", 0], ["seconds", 100], ["seconds", -100], ["seconds", 77], ["seconds", -77],
    ["minutes", 0], ["minutes", 100], ["minutes", -100], ["minutes", 77], ["minutes", -77],
    ["hours", 0], ["hours", 100], ["hours", -100], ["hours", 77], ["hours", -77],
    ["days", 0], ["days", 100], ["days", -100], ["days", 77], ["days", -77],
    ["weeks", 0], ["weeks", 100], ["weeks", -100], ["weeks", 77], ["weeks", -77]
]

DATE_ADD_REPLACE_TEST_MONTHS_YEARS_PARAMS = [
    ["months", 0], ["months", 100], ["months", -100], ["months", 77], ["months", -77],
    ["years", 0], ["years", 100], ["years", -100], ["years", 77], ["years", -77]
]


class TestParsersGeneral(unittest.TestCase):
    @parameterized.expand([["", ], [None, ], ["    "], [" "], ])
    def test_parse_success_empty_string(self, text):
        self.assertIsNone(parse_token(text))


class TestParsersNow(unittest.TestCase):
    def test_parse_success_now_wo_ref(self):
        now = datetime.now()
        parsed_token = parse_token("$now()")
        self.assertIsInstance(parsed_token, datetime)
        self.assertGreaterEqual(parsed_token, now)
        self.assertIsNone(parsed_token.tzinfo)

    def test_parse_success_utc_now_wo_ref(self):
        now = datetime.utcnow().astimezone(pytz.utc)
        parsed_token = parse_token("$utcNow()")

        self.assertIsInstance(parsed_token, datetime)
        self.assertGreaterEqual(parsed_token, now)
        self.assertEqual(parsed_token.tzinfo, pytz.utc)

    def test_parse_success_now_w_ref(self):
        now = datetime.now()
        now_str = now.strftime(ISO8601_DATE_FORMAT_LOCAL)
        parsed_token = parse_token(f"$now({now_str})")

        self.assertIsInstance(parsed_token, datetime)
        self.assertEqual(parsed_token, now)
        self.assertIsNone(parsed_token.tzinfo)

    def test_parse_success_utc_now_w_ref(self):
        now = datetime.utcnow().astimezone(pytz.utc)
        now_str = now.strftime(ISO8601_DATE_FORMAT_UTC)
        parsed_token = parse_token(f"$utcNow({now_str})")

        self.assertIsInstance(parsed_token, datetime)
        self.assertEqual(parsed_token, now)
        self.assertEqual(parsed_token.tzinfo, pytz.utc)


class TestParsersDateAdd(unittest.TestCase):
    def test_parse_success_date_add_no_replace(self):
        now = datetime.now()
        now_str = now.strftime(ISO8601_DATE_FORMAT_UTC)
        result = parse_token(f"$dateAdd({now_str[:-1]})")
        self.assertEqual(now, result)

    def test_parse_success_date_add_no_replace_utc(self):
        now = datetime.utcnow().astimezone(pytz.utc)
        now_str = now.strftime(ISO8601_DATE_FORMAT_UTC)
        result = parse_token(f"$dateAdd({now_str})")
        self.assertEqual(now, result)

    @parameterized.expand(DATE_ADD_REPLACE_TEST_PARAMS)
    def test_parse_success_date_add_replace(self, to_replace: str, value: int):
        now = datetime.now()
        now_str = now.strftime(ISO8601_DATE_FORMAT_LOCAL)
        result = parse_token(f"$dateAdd({now_str}, {{\"{to_replace}\": {value}}})")
        self.assertEqual(now + timedelta(**{to_replace: value}), result)

    @parameterized.expand(DATE_ADD_REPLACE_TEST_MONTHS_YEARS_PARAMS)
    def test_parse_success_date_add_replace_weeks_years(self, to_replace: str, value: int):
        now = datetime.now()
        now_str = now.strftime(ISO8601_DATE_FORMAT_LOCAL)
        result = parse_token(f"$dateAdd({now_str}, {{\"{to_replace}\": {value}}})")
        self.assertEqual(now + relativedelta(**{to_replace: value}), result)

    @parameterized.expand(DATE_ADD_REPLACE_TEST_PARAMS)
    def test_parse_success_date_add_replace_utc(self, to_replace: str, value: int):
        now = datetime.utcnow().astimezone(pytz.utc)
        now_str = now.strftime(ISO8601_DATE_FORMAT_UTC)
        result = parse_token(f"$dateAdd({now_str}, {{\"{to_replace}\": {value}}})")
        self.assertEqual(now + timedelta(**{to_replace: value}), result)

    @parameterized.expand(DATE_ADD_REPLACE_TEST_MONTHS_YEARS_PARAMS)
    def test_parse_success_date_add_replace_weeks_years_utc(self, to_replace: str, value: int):
        now = datetime.utcnow().astimezone(pytz.utc)
        now_str = now.strftime(ISO8601_DATE_FORMAT_UTC)
        result = parse_token(f"$dateAdd({now_str}, {{\"{to_replace}\": {value}}})")
        self.assertEqual(now + relativedelta(**{to_replace: value}), result)

    def test_parse_success_date_add_replace_multi(self):
        now = datetime.now()
        now_str = now.strftime(ISO8601_DATE_FORMAT_LOCAL)
        result = parse_token(f"$dateAdd({now_str}, {{\"minutes\": 120, \"hours\":-2}})")
        self.assertEqual(now, result)

    def test_parse_success_date_add_replace_multi_utc(self):
        now = datetime.utcnow().astimezone(pytz.utc)
        now_str = now.strftime(ISO8601_DATE_FORMAT_UTC)
        result = parse_token(f"$dateAdd({now_str}, {{\"minutes\": 120, \"hours\":-2}})")
        self.assertEqual(now, result)


class TestParsersInt(unittest.TestCase):
    @parameterized.expand([[0, 1], [0, 0], [1, 5], [5, 5], [-5, -5], [-5, 5], ])
    def test_parse_success_int_between(self, a, b):
        result = parse_token(f"$int({a}, {b})")
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, a)
        self.assertLessEqual(result, b)

    @parameterized.expand([[0, ], [1, ], [10, ], [-5, ], ])
    def test_parse_success_int_exact(self, a):
        result = parse_token(f"$int({a})")
        self.assertIsInstance(result, int)
        self.assertEqual(result, a)

    @parameterized.expand([[0, 1, 2], [0, 0, 0], [1, 5, 7], [5, 5, 5], [-5, -5, -5], [-5, 5, 10], ])
    def test_parse_success_int_rnd_choice(self, a, b, c):
        result = parse_token(f"$int({a}, {b}, {c})")
        self.assertIsInstance(result, int)
        self.assertIn(result, [a, b, c])


class TestParsersFloat(unittest.TestCase):
    @parameterized.expand([[0.5, 1.0], [0.0, 0.0], [1.0005, 5.57], [5.3, 5.4], [-5.321, -5.11], [-5.25, 5.25], ])
    def test_parse_success_float_between(self, a, b):
        result = parse_token(f"$float({a}, {b})")
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, a)
        self.assertLessEqual(result, b)

    @parameterized.expand([[0.00001, ], [1.5, ], [10.42, ], [-5.004522, ], ])
    def test_parse_success_float_exact(self, a):
        result = parse_token(f"$float({a})")
        self.assertIsInstance(result, float)
        self.assertEqual(result, a)

    @parameterized.expand([
        [0.0001, 1.054, 2.10], [0.0, 0.0, 0.0], [1.57, 5.9, 7.4], [5.9, 5.8, 5.7],
        [-5.67, -5.12, -5.57], [-5.5, 5.8, 10.12],
    ])
    def test_parse_success_float_rnd_choice(self, a, b, c):
        result = parse_token(f"$float({a}, {b}, {c})")
        self.assertIsInstance(result, float)
        self.assertIn(result, [a, b, c])


class TestParsersIncBy(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        parse_token(f"$incReset()")

    @parameterized.expand([
        [0, 0],
        [1, 1],
        [2, 3],
        [2, 5],
        [3, 8],
        [5, 13]
    ])
    def test_parse_success_inc_w_inc_by(self, inc_by, expected):
        result = parse_token(f"$inc({inc_by})")
        self.assertIsInstance(result, int)
        self.assertEqual(expected, result)


class TestParsersIncByDefault(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        parse_token(f"$incReset()")

    @parameterized.expand([
        [1, ],
        [2, ],
        [3, ],
        [4, ],
        [5, ],
        [6, ]
    ])
    def test_parse_success_inc_wo_inc_by(self, expected):
        result = parse_token(f"$inc()")
        self.assertIsInstance(result, int)
        self.assertEqual(expected, result)


class TestParsersDecBy(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        parse_token(f"$decReset()")

    @parameterized.expand([
        [0, -0],
        [1, -1],
        [2, -3],
        [2, -5],
        [3, -8],
        [5, -13]
    ])
    def test_parse_success_dec_w_inc_by(self, dec_by, expected):
        result = parse_token(f"$dec({dec_by})")
        self.assertIsInstance(result, int)
        self.assertEqual(expected, result)


class TestParsersDecByDefault(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        parse_token(f"$decReset()")

    @parameterized.expand([
        [-1, ],
        [-2, ],
        [-3, ],
        [-4, ],
        [-5, ],
        [-6, ]
    ])
    def test_parse_success_inc_wo_inc_by(self, expected):
        result = parse_token(f"$dec()")
        self.assertIsInstance(result, int)
        self.assertEqual(expected, result)


class TestParsersGuid(unittest.TestCase):
    def test_parse_success_guid(self):
        i = 0
        guids = []
        while i < 100:
            guids.append(parse_token("$guid()"))
            self.assertIsInstance(UUID(guids[-1], version=4), UUID)
            i += 1
        self.assertEqual(100, len(set(guids)))

    def test_parse_success_guid_keep(self):
        i = 0
        guids = []
        while i < 100:
            guids.append(parse_token("$guid(true)"))
            self.assertIsInstance(UUID(guids[-1], version=4), UUID)
            i += 1
        self.assertEqual(1, len(set(guids)))


class TestParsersNext(unittest.TestCase):
    def test_parse_next_str_list(self):
        input_list = ["Foo", "Bar"]

        for input_list_item in input_list:
            parsed = parse_token(f"$next({input_list})")
            self.assertEqual(input_list_item, parsed)

    def test_parse_next_int_list(self):
        input_list = [1, 2, 3]

        for input_list_item in input_list:
            parsed = parse_token(f"$next({input_list})")
            self.assertEqual(input_list_item, parsed)

    def test_parse_next_float_list(self):
        input_list = [1.1, 2.3, 3.44, 5.7]

        for input_list_item in input_list:
            parsed = parse_token(f"$next({input_list})")
            self.assertEqual(input_list_item, parsed)

    def test_parse_next_int_list_repeat(self):
        input_list = [1, 2, 3]

        test_list = input_list*100
        for input_list_item in test_list:
            parsed = parse_token(f"$next({input_list})")
            self.assertEqual(input_list_item, parsed)

    def test_parse_next_float_list_repeat(self):
        input_list = [1.1, 2.3, 3.44, 5.7]

        test_list = input_list*100
        for input_list_item in test_list:
            parsed = parse_token(f"$next({input_list})")
            self.assertEqual(input_list_item, parsed)

    def test_parse_next_string_list_repeat(self):
        input_list = ["bacon", "zitos", "foo", "bar"]

        test_list = input_list*100
        for input_list_item in test_list:
            parsed = parse_token(f"$next({input_list})")
            self.assertEqual(input_list_item, parsed)

    def test_parse_next_empty_list(self):
        input_list = []
        parsed = parse_token(f"$next({input_list})")
        self.assertEqual("$next([])", parsed)

    def test_parse_next_invalid_token(self):
        invalid_input = "$next()"
        parsed = parse_token(invalid_input)
        self.assertEqual(invalid_input, parsed)

    def test_parse_next_invalid_list(self):
        invalid_input = "$next([)"
        parsed = parse_token(invalid_input)
        self.assertEqual(invalid_input, parsed)


if __name__ == '__main__':
    unittest.main()
