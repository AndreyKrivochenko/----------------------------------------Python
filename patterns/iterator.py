from collections.abc import Iterator
from typing import List, Any


class StudentCourseIterator(Iterator):
    _position = None

    def __init__(self, collection: List[Any]):
        self._collection = collection
        self._position = 0

    def __next__(self):
        try:
            value = self._collection[self._position].name
            self._position += 1
        except IndexError:
            raise StopIteration()

        return value
