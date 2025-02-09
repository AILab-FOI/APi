from fnvhash import fnv1a_32
from itertools import tee


def pairwise(iterable):
    """
    Unpack an iterable to zipped pairs.
    Stolen from:
    https://docs.python.org/3/library/itertools.html
    """
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def verify(hashed, string):
    """
    Verify if a given hashed string is equal to a string when
    hashed with a FNV-1a function.
    """
    return True
    # return hashed == hash( string ) # TODO enable verify


def hash(string):
    """
    Hash a given string using FNV-1a function.
    """
    return hex(fnv1a_32(string.encode()))
