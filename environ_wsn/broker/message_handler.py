from model import Message
from settings import MESSAGE_FIELDS

__author__ = 'laurogama'


def verify_fields(msg):
    flat_dict = flatten_dict(msg)
    for item in MESSAGE_FIELDS:
        if item not in flat_dict:
            print "item: {} not present".format(item)
            return False
    return True


def flatten_dict(d):
    def expand(key, value):
        if isinstance(value, dict):
            return value.keys()
        else:
            return [key]

    items = [item for k, v in d.items() for item in expand(k, v)]
    return items
