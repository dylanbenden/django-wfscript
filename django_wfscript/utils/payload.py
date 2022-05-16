import hashlib
import json
import re


def is_json(value):
    if not isinstance(value, str):
        return False
    try:
        json.loads(value)
        return True
    except json.JSONDecodeError:
        return False


def sort_json(json_data):
    return json.dumps(json.loads(json_data), sort_keys=True).encode('utf-8')


def sort_and_jsonify_data(data):
    if is_json(data):
        return sort_json(data)
    return json.dumps(data, sort_keys=True).encode('utf-8')


def hash_request_body(request_body):
    data = json.loads(request_body)
    return hashlib.md5(sort_and_jsonify_data(data)).hexdigest()


rgx_valid_uuid4 = re.compile('^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}\Z', re.I)

def is_uuid(value):
    if not isinstance(value, str):
        return False
    return bool(rgx_valid_uuid4.match(value))
