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

def local_map(x, inmin, inmax, tomin, tomax) -> float:
    return (x-inmin)*(tomax-tomin) / (inmax-inmin)+tomin

def count_values(config: Database) -> None:
    living_peoples = config.living.area / config.living.rate + config.appartaments.area / config.appartaments.rate
    
    working_peoples = living_peoples * config.working_capacity * config.peak_hour_load.for_residents
    office_peoples = config.office.area / config.office.rate * config.peak_hour_load.for_offices
    total_peoples = working_peoples + office_peoples
    
    social_transport = total_peoples * (1-config.personal_transport_rate) 
    personal_transopt = (total_peoples - social_transport) / config.auto_occupancy_rate

    road_load = personal_transopt / len(config.roads)
    output = [[], [], round(personal_transopt), round(social_transport), round(total_peoples), config.appartaments.area, config.living.area, config.office.area]

    for road in config.roads: 
        ort = road_load + road.basic_traffic
        persent = (round(ort) / road.bandwidth*10)
        ball = round(local_map(persent, 0, 99, 0, 10)) if persent < 100 else 11
        data = [road.id, round(ort), ball, round(persent, 2)]
        output[0].append(data)

    metro_load = social_transport / len(config.metro_stantions)

    for metro in config.metro_stantions:
        omt = metro_load + metro.basic_traffic
        persent = omt / metro.bandwidth * 100
        data = [metro.id, round(omt), True if omt <= metro.bandwidth else False, round(persent, 2)]
        output[1].append(data)

    return output

def search_by_id(id: int, data: Database) -> TransportObject | None:
    elements = data.metro_stantions + data.roads
    for element in elements:
        if element.id == id: return element
    return None

def get_endword_by_plural(number: int) -> str:
    if number in (11, 12, 13, 14): return 'ов'
    elif number % 10 == 1: return ''
    elif number % 10 in (2, 3, 4): return 'а'
    return 'ов'

def clear_all_values(config: Database) -> None:
    config.appartaments.area = 0
    config.living.area = 0
    config.office.area = 0
    save_database(config.dict())

def get_all_areas(config: Database) -> list:
    return [config.appartaments.area, config.living.area, config.office.area]

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