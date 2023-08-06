# -*- coding: utf-8 -*-
import ast
from datetime import datetime
from pprint import pprint

from parsers import parse_token

ISO8601_DATE_FORMAT_UTC = "%Y-%m-%dT%H:%M:%S.%fZ"
ISO8601_DATE_FORMAT_LOCAL = ISO8601_DATE_FORMAT_UTC[:-1]
JSON_TEMPLATE = """{
    "id": "$inc()",
    "testSession": "$guid(true)",
    "name": "Dolly",
    "age": "$int(18, 42)",
    "score": "$float(150, 9999)",
    "status": "$int(1,2,3,4,5)",
    "generationDate": "$utcNow()"    
}"""


def create_test_data_from_template():
    test_items = []
    template = ast.literal_eval(JSON_TEMPLATE)
    test_data_creation_start = datetime.utcnow()

    created_at_delay = {"minutes": 15}

    for i in range(50):
        test_item = {}
        for key, item in template.items():
            test_item[key] = parse_token(item)

        test_item["createdAt"] = parse_token(
            f"$dateAdd({test_data_creation_start.strftime(ISO8601_DATE_FORMAT_UTC)}, {created_at_delay})")

        test_data_creation_start = test_item["createdAt"]
        test_items.append(test_item)

    pprint(test_items)


if __name__ == '__main__':
    create_test_data_from_template()
