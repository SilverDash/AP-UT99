from enum import IntEnum
from typing import NamedTuple, Optional
from BaseClasses import Location, Item, ItemClassification


class UTLocation(Location):
    game = "Unreal Tournament"


class UTItem(Item):
    game = "Unreal Tournament"


class Difficulty(IntEnum):
    Novice = 1
    Average = 2
    Experienced = 3
    Skilled = 4
    Adept = 5
    Masterful = 6
    Inhuman = 7
    Godlike = 8


class LocData(NamedTuple):
    id: int = 0
    region: str = ""
    required_ladderItem: list[str] = []
    needs_previous_map: bool = True
    map_item_orderID: int = 0
    misc_required: list[str] = []


class ItemData(NamedTuple):
    code: Optional[int]
    classification: ItemClassification