from datetime import datetime
from dataclasses_avroschema import AvroModel

class Data(AvroModel):
    def to_json(self) -> str:
        """Convert the object to its JSON representation."""
        raise NotImplementedError

    @property
    def unique_identifier(self) -> str:
        """Return a unique identifier for the object."""
        raise NotImplementedError

    @property
    def timestamp(self) -> datetime:
        """Return the timestamp of the data."""
        raise NotImplementedError