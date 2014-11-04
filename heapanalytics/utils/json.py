# coding=utf-8
from __future__ import unicode_literals, absolute_import

"""
Get the JSON implementation.

"""

try:
    # Try for ujson first because it is very fast
    import ujson

    def dumps(obj, *args, **kwargs):
        # ujson dumps method doesn't have separators keyword argument
        if 'separators' in kwargs:
            del kwargs['separators']
        return ujson.dumps(obj, *args, **kwargs)

    def loads(self, str, *args, **kwargs):
        return ujson.loads(str, *args, **kwargs)

except ImportError:
    try:
        import simplejson as json
    except ImportError:
        import json

    def dumps(obj, *args, **kwargs):
        return json.dumps(obj, *args, **kwargs)

    def loads(str, *args, **kwargs):
        return json.loads(str, *args, **kwargs)
