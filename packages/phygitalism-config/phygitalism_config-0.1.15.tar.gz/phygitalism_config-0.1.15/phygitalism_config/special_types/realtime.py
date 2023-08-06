from typing import TypeVar, Generic

T = TypeVar('T')


class Realtime(Generic[T]):

    def __init__(self, _type: T):
        self._type = _type

    def get_type(self) -> T:
        return self._type

    @classmethod
    def __class_getitem__(cls, item: T):
        return Realtime(item)
