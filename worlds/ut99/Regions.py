import collections

from BaseClasses import Region, Entrance, ItemClassification, Location, LocationProgressType
from .Locations import location_table
from typing import TYPE_CHECKING, List, Dict
from .Options import RandomItemsPerMap,ExtraLadders,CustomMapRanges,ExtraLaddersNumber,VaryRandomMapNumber,MapsPerAS,MapsPerCTF,MapsPerDM,MapsPerDOM,MapsPerEX,MapsPerEX2,MapsPerEX3,MapsPerTDM
import random

from .Types import UTLocation

if TYPE_CHECKING:
    from . import UT99World


#Setting up the iterables for the globals. probably a better way to do this
TDMRange = ()
DMRange  = ()
ASRange  = ()
DOMRange = ()
CTFRange = ()
EXRange  = ()
EX2Range = ()
EX3Range = ()
limit = int




def set_mapranges(world: "UT99World"):
    global limit
    limit = world.options.RandomItemsPerMap.value
    """Initialize the random ranges the map count rando will use.
    Uses random.randrange and user options settings
    Globals are used to allow the varables be used in other parts of this module."""
    global TDMRange, DMRange, ASRange, DOMRange, CTFRange, EXRange, EX2Range, EX3Range
    #Random full
    if VaryRandomMapNumber:
        TDMRange = range(MapsPerTDM.range_start,random.randrange(MapsPerTDM.range_start,21))
        DMRange = range(MapsPerDM.range_start, random.randrange(MapsPerDM.range_start, 21))
        ASRange = range(MapsPerAS.range_start, random.randrange(MapsPerAS.range_start, 21))
        DOMRange = range(MapsPerDOM.range_start, random.randrange(MapsPerDOM.range_start, 21))
        CTFRange = range(MapsPerCTF.range_start, random.randrange(MapsPerCTF.range_start, 21))
        if ExtraLadders:
            EXRange = range(MapsPerEX.range_start, random.randrange(MapsPerEX.range_start, 21))
            EX2Range = range(MapsPerEX2.range_start, random.randrange(MapsPerEX2.range_start, 21))
            EX3Range = range(MapsPerEX3.range_start, random.randrange(MapsPerEX3.range_start, 21))
    #exact custom range
    elif CustomMapRanges:
        TDMRange = range(MapsPerTDM.range_start, world.options.MapsPerTDM.value+1)
        DMRange = range(MapsPerDM.range_start, world.options.MapsPerTDM.value+1)
        ASRange = range(MapsPerAS.range_start,  world.options.MapsPerTDM.value+1)
        DOMRange = range(MapsPerDOM.range_start, world.options.MapsPerTDM.value+1)
        CTFRange = range(MapsPerCTF.range_start,  world.options.MapsPerTDM.value+1)
        if ExtraLadders:
            EXRange = range(MapsPerEX.range_start,  world.options.MapsPerTDM.value+1)
            EX2Range = range(MapsPerEX2.range_start,  world.options.MapsPerTDM.value+1)
            EX3Range = range(MapsPerEX3.range_start,  world.options.MapsPerTDM.value+1)
    #default values
    else:
        TDMRange = range(MapsPerTDM.range_start)
        DMRange = range(MapsPerDM.range_start)
        ASRange = range(MapsPerAS.range_start)
        DOMRange = range(MapsPerDOM.range_start)
        CTFRange = range(MapsPerCTF.range_start)
        if ExtraLadders:
            EXRange = range(MapsPerEX.range_start)
            EX2Range = range(MapsPerEX2.range_start)
            EX3Range = range(MapsPerEX3.range_start)


# This is actually a pretty good way to do region and connections
UT_region_connections: Dict[str, List[str]] = {
    "Menu":["LadderScreen"],
    "LadderScreen":["DM","DOM","TDM","CTF","AS","EX","EX2","EX3","Challenge"],

     **{f"DM {i}": [f"DM {j}"] for i, j in zip(DMRange, DMRange[1:])},
    f"DM {DMRange[-1]}": [],

     **{f"DOM {i}": [f"DOM {j}"] for i, j in zip(DOMRange, DOMRange[1:])},
    f"DOM {DOMRange[-1]}": [],

     **{f"CTF {i}": [f"CTF {j}"] for i, j in zip(CTFRange, CTFRange[1:])},
    f"CTF {CTFRange[-1]}": [],

     **{f"AS {i}": [f"AS {j}"] for i, j in zip(ASRange, ASRange[1:])},
    f"AS {ASRange[-1]}": [],

     **{f"EX {i}": [f"EX {j}"] for i, j in zip(EXRange, EXRange[1:])},
    f"EX {EXRange[-1]}": [],

     **{f"EX2 {i}": [f"EX2 {j}"] for i, j in zip(EX2Range, EX2Range[1:])},
    f"EX2 {EX2Range[-1]}": [],

    **{f"EX3 {i}": [f"EX3 {j}"] for i, j in zip(EX3Range, EX3Range[1:])},
    f"EX3 {EX3Range[-1]}": [],

    **{f"TDM {i}": [f"TDM {j}"] for i, j in zip(TDMRange, TDMRange[1:])},
    f"TDM {TDMRange[-1]}": [],

    "Challenge":   ["Challenge 1"],
    "Challenge 1": ["Challenge 2"],
    "Challenge 2": ["Challenge 3"]

}

UT_EX_region_Connections:Dict[str,List[str]] = {
    "EX": [f"EX {i}" for i in EXRange],

    "EX2": [f"EX2 {i}" for i in EX2Range],

    "EX3": [f"EX3 {i}" for i in EX3Range],
}

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
    world.multiworld.regions.append(reg)
    return reg


# don't judge. It's not the size that matters
def _tinyhelper(num:int):
    if num == 1:
        return MapsPerEX2
    return MapsPerEX3


# don't use this, don't read this
def _make_theEXladderList(count1=0)-> Dict[str,List[str]]:
    #ex1 is a static EX string
    ex1 = {"EX": [f"EX {i}" for i in range(1,MapsPerEX)]}
    #But ex2 can be a 2 or 3
    if count1 != 0:
        ex2 = {f"EX{count1}": [f"EX {i}" for i in range(1,_tinyhelper(count1))]}
        ex1.update(ex2)
    return ex1


def create_regions(world: "UT99World") -> Dict[str, Region]:
    _local_table = {}
    _local_table.update(UT_region_connections)
    if ExtraLadders:
        _local_table.update(_make_theEXladderList(ExtraLaddersNumber.value))
    return {name: create_region(world, name) for name in _local_table}


def create_all_regions_and_connections(world: "UT99World") -> None:
    created_regions = create_regions(world)
    create_connections(world.player, created_regions)
    #create_all_events(world, created_regions)
    world.multiworld.regions += created_regions.values()


# An "Entrance" is really just a connection between two regions
def create_entrance(world: "UT99World", player: int, source: str, destination: str, regions: Dict[str, Region]) -> Entrance:
    entrance = Entrance(player, f"From {source} To {destination}", regions[source])
    entrance.connect(regions[destination])
    return entrance


def create_connections(player: int, regions: Dict[str, Region]) -> None:
    for source, destinations in UT_region_connections.items():
        if destinations is not None:
            new_entrances = [create_entrance(player, source, destination, regions) for destination in destinations]
            regions[source].exits = new_entrances