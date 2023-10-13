from typing import Generic, TypeVar, Iterator, List
T = TypeVar('T')  # This will allow the DataLoader interface to be generic

class DataLoader(Generic[T]):
    def get_entries_in_order(self) -> Iterator[T]:
        raise NotImplementedError

    def get_batches(self) -> Iterator[List[T]]:
        raise NotImplementedError
