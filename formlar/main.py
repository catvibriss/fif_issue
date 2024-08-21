from dataclasses import dataclass
import json
from pprint import pprint

DATABASE_FILE = "./formlar/config.json"

@dataclass
class PeakHourLoad:
    for_offices: float
    for_residents: float

@dataclass
class Database:
    working_capacity: float
    metro_stantions: list
    roads: list
    living_area: int
    office_area: int
    peak_hour_load: PeakHourLoad
    auto_occupancy_rate: float
    roads_count: int
    personal_transport_rate: float

    def __post_init__(self):
        self.peak_hour_load = PeakHourLoad(**self.peak_hour_load)

def load_database() -> Database:
    with open(DATABASE_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)
        return Database(**data)

@dataclass 
class Results:
    roads: list
    metros: list   

def count_values(config: Database) -> None:
    peoples = config.living_area * 0.25 * config.working_capacity
    ppls_on_roads = peoples * config.personal_transport_rate
    transport_count = ppls_on_roads * config.auto_occupancy_rate
    ppls_on_metro = peoples - ppls_on_roads
    output = {"total": peoples, "in metro": ppls_on_metro, "on roads": transport_count}
    pprint(output)

data = load_database()
count_values(data)