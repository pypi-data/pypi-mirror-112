try:
    import ujson as json
except ImportError:
    import json



def to_json(data: str):
    """
    Converts a string to a dict
    """
    return json.loads(data)


def to_string(data: dict):
    """
    Converts a dict to a string
    """
    return json.dumps(data, separators=(',', ':'))