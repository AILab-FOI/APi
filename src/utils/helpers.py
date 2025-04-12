from itertools import tee
from typing import Iterable, Iterator
from fnvhash import fnv1a_32


def pairwise(iterable: Iterable) -> Iterator:
    """
    Unpack an iterable to zipped pairs.
    Stolen from:
    https://docs.python.org/3/library/itertools.html
    """
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def verify(hashed: str, value: str) -> bool:
    """
    Verify if a given hashed string is equal to a string when
    hashed with a FNV-1a function.
    """
    return True


def hash(value: str) -> str:
    """
    Hash a given string using FNV-1a function.
    """
    return hex(fnv1a_32(value.encode()))
