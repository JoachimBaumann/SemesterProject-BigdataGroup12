import datetime
from dataclasses import asdict, dataclass
import json
from models.interfaces import Data

from utils.serializer import datetime_serializer

@dataclass
class TaxiData(Data):
    vendorid: int
    tpep_pickup_datetime: datetime.datetime
    tpep_dropoff_datetime: datetime.datetime
    passenger_count: int
    trip_distance: float
    ratecodeid: int
    store_and_fwd_flag: bool
    pulocationid: int
    dolocationid: int
    payment_type: int
    fare_amount: float
    extra: float
    mta_tax: float
    tip_amount: float
    tolls_amount: float
    improvement_surcharge: float
    total_amount: float
    congestion_surcharge: str

    @property
    def unique_identifier(self) -> str:
        return str(self.vendorid)

    @property
    def timestamp(self) -> datetime:
        return self.tpep_pickup_datetime

    def to_json(self):
        return json.dumps(asdict(self), default=datetime_serializer)

    def __lt__(self, other: 'TaxiData'):    
        return self.tpep_pickup_datetime < other.tpep_pickup_datetime
