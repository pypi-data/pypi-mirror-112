from typing import Generic, Sequence, Tuple, TypeVar, Union

from bisect import bisect_left, bisect_right

T = TypeVar("T")
K = TypeVar("K")


class Index(Generic[K, T]):
    """
    Class to provide efficient indexing and slicing operations into a list of objects by certain attribute key.

    This with *only* work if:
    - The list is sorted
    - The list doesn't change

    I have not tested how this will handle duplicate values.
    """

    def __init__(self, items: Sequence[T], keyattr: str):
        self.items = items
        self.keys: Tuple[K] = tuple(getattr(i, keyattr) for i in items)

    def __getitem__(self, key: Union[slice, K]) -> T:
        if not isinstance(key, slice):
            return self.eq(key)

        start_index = key.start
        if start_index is not None:
            start_index = self.gteq_index(start_index)
            if start_index is None:
                return []

        stop_index = key.stop
        if stop_index is not None:
            stop_index = self.gteq_index(stop_index)

        return self.items[start_index:stop_index:key.step]

    def eq(self, key: K) -> T:
        index = self.eq_index(key)
        if index is None:
            return None
        return self.items[index]

    def lteq(self, key: K) -> T:
        index = self.lteq_index(key)
        if index is None:
            return None
        return self.items[index]

    def lt(self, key: K) -> T:
        index = self.lt_index(key)
        if index is None:
            return None
        return self.items[index]

    def gteq(self, key: K) -> T:
        index = self.gteq_index(key)
        if index is None:
            return None
        return self.items[index]

    def gt(self, key: K) -> T:
        index = self.gt_index(key)
        if index is None:
            return None
        return self.items[index]

    def eq_index(self, key: K) -> int:
        index = self.gteq_index(key)
        if index is None:
            return None
        if self.keys[index] != key:
            return None
        return index

    def lteq_index(self, key: K) -> int:
        index = bisect_right(self.keys, key) - 1
        if index == -1:
            return None
        return index

    def lt_index(self, key: K) -> int:
        index = bisect_left(self.keys, key) - 1
        if index == -1:
            return None
        return index

    def gt_index(self, key: K) -> int:
        index = bisect_right(self.keys, key)
        if index == len(self.keys):
            return None
        return index

    def gteq_index(self, key: K) -> int:
        index = bisect_left(self.keys, key)
        if index == len(self.keys):
            return None
        return index
