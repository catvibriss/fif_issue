from dataclasses import dataclass, asdict
import json
from pprint import pprint

DATABASE_FILE = "./formlar/config.json"

@dataclass
class PeakHourLoad:
    for_offices: float
    for_residents: float
    
    def dict(self) -> dict:
        return self.__dict__
    
@dataclass 
class TransportObject:
    id: int
    name: str
    object_type: str
    bandwidth: float

    def dict(self) -> dict:
        return self.__dict__

@dataclass 
class AreaObject:
    area: int
    rate: int

    def dict(self) -> dict:
        return self.__dict__

@dataclass
class Database:
    working_capacity: float
    metro_stantions: list[TransportObject]
    roads: list[TransportObject]
    living: AreaObject
    office: AreaObject
    appartaments: AreaObject
    peak_hour_load: PeakHourLoad
    auto_occupancy_rate: float
    personal_transport_rate: float

    def __post_init__(self):
        self.peak_hour_load = PeakHourLoad(**self.peak_hour_load)
        self.appartaments = AreaObject(**self.appartaments)
        self.office = AreaObject(**self.office)
        self.living = AreaObject(**self.living)
        for i in range(len(self.roads)): self.roads[i] = TransportObject(**self.roads[i])
        for i in range(len(self.metro_stantions)): self.metro_stantions[i] = TransportObject(**self.metro_stantions[i])

    def dict(self) -> dict:
        dict = self.__dict__
        dict['peak_hour_load'] = self.peak_hour_load.dict()
        dict['appartaments'] = self.appartaments.dict()
        dict['office'] = self.office.dict()
        dict['living'] = self.living.dict()
        dict["roads"] = [item.dict() for item in self.roads]
        dict['metro_stantions'] = [item.dict() for item in self.metro_stantions]
        return dict
    
def load_database() -> Database:
    with open(DATABASE_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)
        return Database(**data)

def save_config(new_dict: dict) -> None:
    with open(DATABASE_FILE, "w", encoding="utf-8") as file:
        json.dump(new_dict, file, indent=4, sort_keys=True, ensure_ascii=False)

def count_values(config: Database) -> None:
    

data = load_database()
save_config(data.dict())
count_values(data)