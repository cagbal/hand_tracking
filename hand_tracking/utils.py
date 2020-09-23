from collections.abc import Iterable


def count_None(iterable):
    assert isinstance(iterable, Iterable), "Input must be an iterable"

    count = 0

    for x in iterable:
        if isinstance(x, type(None)):
            count += 1

    return count