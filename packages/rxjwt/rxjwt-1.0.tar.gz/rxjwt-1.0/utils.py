from base64 import urlsafe_b64encode
from importlib import import_module
from uuid import uuid4


def string_as_base64(string):
    """
    Converts a utf-8 string to url save base64.
    :param string: The string to convert.
    :return: Bytes containing base64-encoded input string.
    """
    return urlsafe_b64encode(bytes(string, "utf-8"))


def generate_secret():
    """
    Generates new server secret value.
    :return: The secret value which will be used in token creation.
    """
    return bytes(str(uuid4()), "utf-8")


def import_class(class_name):
    attr = class_name.split(".")[-1]
    module = class_name.replace(".%s" % attr, "")
    return getattr(import_module(module), attr)
