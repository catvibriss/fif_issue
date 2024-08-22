from dataclasses import dataclass
import json
from pprint import pprint

DATABASE_FILE = "./formulas/config.json"

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
    basic_traffic: float
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

def save_database(new_dict: dict) -> None:
    with open(DATABASE_FILE, "w", encoding="utf-8") as file:
        json.dump(new_dict, file, indent=4, sort_keys=True, ensure_ascii=False)

def count_values(config: Database) -> None:
    living_peoples = config.living.area / config.living.rate + config.appartaments.area / config.appartaments.rate
    
    working_peoples = living_peoples * config.working_capacity * config.peak_hour_load.for_residents
    office_peoples = config.office.area / config.office.rate * config.peak_hour_load.for_offices
    total_peoples = working_peoples + office_peoples
    
    social_transport = total_peoples * (1-config.personal_transport_rate) 
    personal_transopt = (total_peoples - social_transport) / config.auto_occupancy_rate

    road_load = personal_transopt / len(config.roads)
    output = [[], [], round(personal_transopt), round(social_transport), round(total_peoples)]

    for road in config.roads: 
        ort = road_load + road.basic_traffic
        data = [road.id, round(ort), round(ort/road.bandwidth)]
        output[0].append(data)

    metro_load = social_transport / len(config.metro_stantions)

    for metro in config.metro_stantions:
        omt = metro_load + metro.basic_traffic
        data = [metro.id, round(omt), True if omt <= metro.bandwidth else False]
        output[1].append(data)

    return output

def search_by_id(id: int, data: Database) -> TransportObject | None:
    elements = data.metro_stantions + data.roads
    for element in elements:
        if element.id == id: return element
    return None

if __name__ == '__main__': # для тестов
    data = load_database()
    pprint(count_values(data))
    

'''
что значит вывод
возвращается список из 4-ёх элементов:
1: список с дорогами
- один элемент - одна дорога
- в каждом подсписке дорог три элемента: id, трафик (транспортные средства/час), баллы пробок (в таком порядке)
2: список со станциями
- один элемент - одна станция
- в каждом подсписке три элемента: id, трафик (тыс.чел./час), доступность станции (False - перегружена, True - нормально)
3: общее кол-во машин
4: общее кол-во людей на ОТ
5: общее кол-во людей в потоке
'''