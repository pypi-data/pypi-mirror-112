import itertools
from typing import Iterable, Generator


def grouper(n: int, iterable: Iterable) -> Generator:
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, n))
        if not chunk:
            return
        yield chunk
