from schema import Schema, And, Or, Use, Optional, Literal
import validators

# def Xor(*args, **kwargs):
#     kwargs["only_one"] = True
#     return Or(*args, **kwargs)

def Nullable(validator):
    return Schema(Or(validator, None), description="Can be None if evaluated to False")

def HasKey(key):
    return Schema(lambda d: isinstance(d, dict) and key in d, name="has key {key}".format(key=key))

import re

# https://stackoverflow.com/questions/7160737/python-how-to-validate-a-url-in-python-malformed-or-not/7160778
# URL_REG = re.compile(
#     r'^(?:http|ftp)s?://'  # http:// or https://
#     r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  #domain...
#     r'localhost|'  #localhost...
#     r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
#     r'(?::\d+)?'  # optional port
#     r'(?:/?|[/?]\S+)$',
#     re.IGNORECASE
# )

# Url = Schema(
#     lambda url: re.match(URL_REG, url) is not None, name="is URL")

Url = Schema(
    lambda url: validators.url(url), name="is URL")

class List:
    def __init__(self, callable_):
        self._callable = callable_
    def validate(self, data):
        if not isinstance(data, list):
            data = [data]
        return Schema([self._callable], name="Ensure List").validate(data)