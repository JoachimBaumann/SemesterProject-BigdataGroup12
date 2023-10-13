import datetime
from dataclasses import asdict, dataclass, field
from dateutil.parser import parse as date_parse
import json

from utils.serializer import datetime_serializer

@dataclass
class BusData:
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
    
    def to_json(self):
        return json.dumps(asdict(self), default=datetime_serializer)

    def __lt__(self, other: 'BusData'):    
        return self.RecordedAtTime < other.RecordedAtTime