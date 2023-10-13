from typing import Iterable, Generator, Tuple, TypeVar
from collections import deque
from itertools import islice

T = TypeVar('T')

def sliding_window(iterable: Iterable[T], size: int = 2) -> Generator[Tuple[T, ...], None, None]:
    """Generates a sliding window over the iterable."""
    it = iter(iterable)
    win = deque(islice(it, size), maxlen=size)
    for item in it:
        yield tuple(win)
        win.append(item)
