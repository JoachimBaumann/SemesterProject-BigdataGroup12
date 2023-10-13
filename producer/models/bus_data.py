import datetime
from dataclasses import asdict, dataclass, field
import json
from models.interfaces import Data

from utils.serializer import datetime_serializer

@dataclass
class BusData(Data):
    RecordedAtTime: datetime.datetime = field(compare=True)
    DirectionRef: int
    PublishedLineName: str
    OriginName: str
    OriginLat: float
    OriginLong: float
    DestinationName: str 
    DestinationLat: float
    DestinationLong: float
    VehicleRef: str
    VehicleLocationLatitude: float
    VehicleLocationLongitude: float 
    NextStopPointName: str
    ArrivalProximityText: str
    DistanceFromStop: int 
    ExpectedArrivalTime: str
    ScheduledArrivalTime: str
    
    @property
    def unique_identifier(self) -> str:
        return self.VehicleRef
    
    @property
    def timestamp(self) -> datetime:
        return self.RecordedAtTime

    def to_json(self):
        return json.dumps(asdict(self), default=datetime_serializer)

    def __lt__(self, other: 'BusData'):    
        return self.RecordedAtTime < other.RecordedAtTime