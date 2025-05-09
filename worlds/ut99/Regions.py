import collections

from BaseClasses import Region, Entrance, ItemClassification, Location, LocationProgressType
from .Locations import location_table,Ladder_Completion_TDM,Ladder_Completions_EX
from typing import TYPE_CHECKING, List, Dict
from .Options import MapsPerAS,MapsPerCTF,MapsPerDM,MapsPerDOM,MapsPerEX,MapsPerEX2,MapsPerEX3,MapsPerTDM
import random

from .Types import UTLocation

if TYPE_CHECKING:
    from . import UT99World


#Setting up the iterables for the globals. probably a better way to do this.....there was

limit = 99


UT_EX_region_Connections:Dict[str,List[str]] = {
    "EX":["EX 1"],
    "EX2":["EX2 1"],
    "EX3":["EX3 1"],}

def set_mapranges(world: "UT99World"):
    global limit
    limit = world.options.RandomItemsPerMap.value
    """Initialize the random ranges the map count rando will use.
    Uses random.randrange and user options settings
    Globals are used to allow the varables be used in other parts of this module."""
    #Random full
    if world.options.VaryRandomMapNumber:
        world.TDMRange = range(MapsPerTDM.range_start,random.randrange(MapsPerTDM.range_start,21))
        world.DMRange = range(MapsPerDM.range_start, random.randrange(MapsPerDM.range_start, 21))
        world.ASRange = range(MapsPerAS.range_start, random.randrange(MapsPerAS.range_start, 21))
        world.DOMRange = range(MapsPerDOM.range_start, random.randrange(MapsPerDOM.range_start, 21))
        world.CTFRange = range(MapsPerCTF.range_start, random.randrange(MapsPerCTF.range_start, 21))
        if world.options.ExtraLadders:
            world.EXRange = range(MapsPerEX.range_start, random.randrange(MapsPerEX.range_start, 21))
            world.EX2Range = range(MapsPerEX2.range_start, random.randrange(MapsPerEX2.range_start, 21))
            world.EX3Range = range(MapsPerEX3.range_start, random.randrange(MapsPerEX3.range_start, 21))
    #exact custom range
    elif world.options.CustomMapRanges:
        world.TDMRange = range(MapsPerTDM.range_start, world.options.MapsPerTDM.value+1)
        world.DMRange = range(MapsPerDM.range_start, world.options.MapsPerTDM.value+1)
        world.ASRange = range(MapsPerAS.range_start,  world.options.MapsPerTDM.value+1)
        world.DOMRange = range(MapsPerDOM.range_start, world.options.MapsPerTDM.value+1)
        world.CTFRange = range(MapsPerCTF.range_start,  world.options.MapsPerTDM.value+1)
        if world.options.ExtraLadders:
            world.EXRange = range(MapsPerEX.range_start,  world.options.MapsPerTDM.value+1)
            world.EX2Range = range(MapsPerEX2.range_start,  world.options.MapsPerTDM.value+1)
            world.EX3Range = range(MapsPerEX3.range_start,  world.options.MapsPerTDM.value+1)
    #default values
    else:
        world.TDMRange = range(MapsPerTDM.range_start)
        world.DMRange = range(MapsPerDM.range_start)
        world.ASRange = range(MapsPerAS.range_start)
        world.DOMRange = range(MapsPerDOM.range_start)
        world.CTFRange = range(MapsPerCTF.range_start)
        if world.options.ExtraLadders:
            world.EXRange = range(MapsPerEX.range_start)
            world.EX2Range = range(MapsPerEX2.range_start)
            world.EX3Range = range(MapsPerEX3.range_start)


def create_DMregion_connections(world:"UT99World") -> Dict[str, List[str]]:
    return {**{f"DM {i}": [f"DM {j}"] for i, j in zip(world.DMRange, world.DMRange[1:])},
            f"DM {world.DMRange[-1]}": ["LadderScreen"]}

def create_TDMregion_connections(world:"UT99World") -> Dict[str, List[str]]:
    return {**{f"TDM {i}": [f"TDM {j}"] for i, j in zip(world.TDMRange, world.TDMRange[1:])},
            f"TDM {world.TDMRange[-1]}": ["LadderScreen"]}

def create_ASregion_connections(world:"UT99World") -> Dict[str, List[str]]:
    return {**{f"AS {i}": [f"AS {j}"] for i, j in zip(world.ASRange, world.ASRange[1:])},
            f"AS {world.ASRange[-1]}": ["LadderScreen"]}

def create_DOMregion_connections(world:"UT99World") -> Dict[str, List[str]]:
    return {**{f"DOM {i}": [f"DOM {j}"] for i, j in zip(world.DOMRange, world.DOMRange[1:])},
            f"DOM {world.DOMRange[-1]}": ["LadderScreen"]}

def create_CTFregion_connections(world:"UT99World") -> Dict[str, List[str]]:
    return {**{f"CTF {i}": [f"CTF {j}"] for i, j in zip(world.CTFRange, world.CTFRange[1:])},
            f"CTF {world.CTFRange[-1]}": ["LadderScreen"]}

def create_EXregion_connections(world:"UT99World") -> Dict[str, List[str]]:
    return {**{f"EX {i}": [f"EX {j}"] for i, j in zip(world.EXRange, world.EXRange[1:])},
            f"EX {world.EXRange[-1]}": ["LadderScreen"],}

def create_EX2region_connections(world:"UT99World") -> Dict[str, List[str]]:
    return {**{f"EX2 {i}": [f"EX2 {j}"] for i, j in zip(world.EX2Range, world.EX2Range[1:])},
            f"EX2 {world.EX2Range[-1]}": ["LadderScreen"]}

def create_EX3region_connections(world:"UT99World") -> Dict[str, List[str]]:
    return {**{f"EX3 {i}": [f"EX3 {j}"] for i, j in zip(world.EX3Range, world.EX3Range[1:])},
            f"EX3 {world.EX3Range[-1]}": ["LadderScreen"]}


# This is actually a pretty good way to do region and connections
UT_region_connections: Dict[str, List[str]] = {
    "Menu":["LadderScreen"],
    "LadderScreen":["DM","DOM","CTF","AS","Challenge"],
    "DM":["DM 1"],
    "DOM":["DOM 1"],
    "CTF":["CTF 1"],
    "AS":["AS 1"],
    "Challenge":   ["Challenge 1"],
    "Challenge 1": ["Challenge 2"],
    "Challenge 2": ["Challenge 3"],
    "Challenge 3": ["Challenge 3"]
}


created_regions_list:Dict[str, Region]={}


# limitless by default and should never cause an error
def create_region(world: "UT99World", name: str) -> Region:
    reg = Region(name, world.player, world.multiworld)
    count = 0
    # need the limit for options
    for (key, data) in location_table.items():
        if data.region == name:
            if count >= limit:
                break
            location = UTLocation(world.player,key,data.id)
            reg.locations.append(location)
            count+=1
    world.multiworld.regions.append(reg)
    return reg


def create_regions(world: "UT99World") -> Dict[str, Region]:
    _local_table:Dict[str, List[str]] = {}
    if world.options.ExtraLadders:
        UT_region_connections["LadderScreen"].append("EX")
        UT_region_connections.update(create_EXregion_connections(world))
        UT_region_connections["LadderScreen"].append("EX2")
        UT_region_connections.update(create_EX2region_connections(world))
        UT_region_connections["LadderScreen"].append("EX3")
        UT_region_connections.update(create_EX3region_connections(world))
    if world.options.AddTDM:
        UT_region_connections.update({"TDM":["TDM 1"]})
        UT_region_connections["LadderScreen"].append("TDM")
        UT_region_connections.update(create_TDMregion_connections(world))
    _local_table.update(UT_region_connections)
    return {name: create_region(world, name) for name in _local_table}


def create_all_regions_and_connections(world: "UT99World") -> None:
    UT_region_connections.update(create_ASregion_connections(world))
    UT_region_connections.update(create_DMregion_connections(world))
    UT_region_connections.update(create_CTFregion_connections(world))
    UT_region_connections.update(create_DOMregion_connections(world))

    created_regions = create_regions(world)
    create_connections(world.player, created_regions)
    #create_all_events(world, created_regions)
    world.multiworld.regions += created_regions_list.values()


# An "Entrance" is really just a connection between two regions
def create_entrance(player: int, source: str, destination: str, regions: Dict[str, Region]) -> Entrance:
    entrance = Entrance(player, f"From {source} To {destination}", regions[source])
    entrance.connect(regions[destination])
    return entrance


def create_connections(player: int, regions: Dict[str, Region]) -> None:
    for source, destinations in UT_region_connections.items():
        if destinations is not None:
            new_entrances = [create_entrance(player, source, destination, regions) for destination in destinations]
            regions[source].exits = new_entrances