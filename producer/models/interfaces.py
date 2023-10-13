from datetime import datetime
from typing import Protocol

class Data(Protocol):
    def to_json(self) -> str:
        """Convert the object to its JSON representation."""
        pass

    @property
    def unique_identifier(self) -> str:
        """Return a unique identifier for the object."""
        pass

    @property
    def timestamp(self) -> datetime:
        """Return the timestamp of the data."""
        pass