import collections

from BaseClasses import Region, Entrance, ItemClassification, Location, LocationProgressType
from .Locations import location_table, Ladder_Completions, Map_locations, create_Ladder_Completions
from typing import TYPE_CHECKING
from .Options import MapsPerAS,MapsPerCTF,MapsPerDM,MapsPerDOM,MapsPerEX,MapsPerEX2,MapsPerEX3,MapsPerTDM

from .Types import UTLocation

if TYPE_CHECKING:
    from . import UT99World


# Setting up the iterables for the globals. probably a better way to do this.....there was


UT_EX_region_Connections:dict[str,list[str]] = {
    "EX":["EX 1"],
    "EX2":["EX2 1"],
    "EX3":["EX3 1"]}

# this will only do anything if the options are set
def set_mapranges(world: "UT99World"):
    """Initialize the random ranges the map count rando will use.
    Uses random.randrange and user options settings
    """
    #Random full
    if world.options.VaryRandomMapNumber:
        world.TDMRange = range(MapsPerTDM.range_start,world.random.randrange(MapsPerTDM.range_start,21))
        world.DMRange = range(MapsPerDM.range_start, world.random.randrange(MapsPerDM.range_start, 21))
        world.ASRange = range(MapsPerAS.range_start, world.random.randrange(MapsPerAS.range_start, 21))
        world.DOMRange = range(MapsPerDOM.range_start, world.random.randrange(MapsPerDOM.range_start, 21))
        world.CTFRange = range(MapsPerCTF.range_start, world.random.randrange(MapsPerCTF.range_start, 21))
        if world.options.ExtraLadders:
            world.EXRange = range(MapsPerEX.range_start, world.random.randrange(MapsPerEX.range_start, 21))
            world.EX2Range = range(MapsPerEX2.range_start, world.random.randrange(MapsPerEX2.range_start, 21))
            world.EX3Range = range(MapsPerEX3.range_start, world.random.randrange(MapsPerEX3.range_start, 21))
    #exact custom range
    elif world.options.CustomMapRanges:
        world.TDMRange = range(world.options.MapsPerDM.value+1)
        world.DMRange = range(world.options.MapsPerDM.value+1)
        world.ASRange = range(world.options.MapsPerAS.value+1)
        world.DOMRange = range(world.options.MapsPerDOM.value+1)
        world.CTFRange = range(world.options.MapsPerCTF.value+1)
        if world.options.ExtraLadders:
            world.EXRange = range(world.options.MapsPerEX.value+1)
            world.EX2Range = range(world.options.MapsPerEX2.value+1)
            world.EX3Range = range(world.options.MapsPerEX3.value+1)


def create_DMregion_connections(world:"UT99World") -> dict[str, list[str]]:
    return {**{f"DM {i}": [f"DM {j}"] for i, j in zip(world.DMRange[1:], world.DMRange[2:])},
            f"DM {world.DMRange[-1]}": ["LadderScreen"]}

def create_TDMregion_connections(world:"UT99World") -> dict[str, list[str]]:
    return {**{f"TDM {i}": [f"TDM {j}"] for i, j in zip(world.TDMRange[1:], world.TDMRange[2:])},
            f"TDM {world.TDMRange[-1]}": ["LadderScreen"]}

def create_ASregion_connections(world:"UT99World") -> dict[str, list[str]]:
    return {**{f"AS {i}": [f"AS {j}"] for i, j in zip(world.ASRange[1:], world.ASRange[2:])},
            f"AS {world.ASRange[-1]}": ["LadderScreen"]}

def create_DOMregion_connections(world:"UT99World") -> dict[str, list[str]]:
    return {**{f"DOM {i}": [f"DOM {j}"] for i, j in zip(world.DOMRange[1:], world.DOMRange[2:])},
            f"DOM {world.DOMRange[-1]}": ["LadderScreen"]}

def create_CTFregion_connections(world:"UT99World") -> dict[str, list[str]]:
    return {**{f"CTF {i}": [f"CTF {j}"] for i, j in zip(world.CTFRange[1:], world.CTFRange[2:])},
            f"CTF {world.CTFRange[-1]}": ["LadderScreen"]}

def create_EXregion_connections(world:"UT99World") -> dict[str, list[str]]:
    return {**{f"EX {i}": [f"EX {j}"] for i, j in zip(world.EXRange[1:], world.EXRange[2:])},
            f"EX {world.EXRange[-1]}": ["LadderScreen"],}

def create_EX2region_connections(world:"UT99World") -> dict[str, list[str]]:
    return {**{f"EX2 {i}": [f"EX2 {j}"] for i, j in zip(world.EX2Range[1:], world.EX2Range[2:])},
            f"EX2 {world.EX2Range[-1]}": ["LadderScreen"]}

def create_EX3region_connections(world:"UT99World") -> dict[str, list[str]]:
    return {**{f"EX3 {i}": [f"EX3 {j}"] for i, j in zip(world.EX3Range[1:], world.EX3Range[2:])},
            f"EX3 {world.EX3Range[-1]}": ["LadderScreen"]}


# This is actually a pretty good way to do region and connections
UT_region_connections: dict[str, list[str]] = {
    "Menu":["LadderScreen"],
    "LadderScreen":["DM","DOM","CTF","AS","Challenge"],
    "DM":["DM 1"],
    "DOM":["DOM 1"],
    "CTF":["CTF 1"],
    "AS":["AS 1"],
    "Challenge":   ["Challenge 1"],
    "Challenge 1": ["Challenge 2"],
    "Challenge 2": ["Challenge 3"],
    "Challenge 3": ["Victory"],
    "Victory":[]
}


def create_region(world: "UT99World", name: str) -> Region:
    return Region(name, world.player, world.multiworld)


def create_regions(world: "UT99World") -> dict[str, Region]:
    # Add extra ladder regions if enabled
    if world.options.ExtraLadders:
        UT_region_connections.setdefault("LadderScreen", []).extend(["EX", "EX2", "EX3"])
        UT_region_connections.update(create_EXregion_connections(world))
        UT_region_connections.update(create_EX2region_connections(world))
        UT_region_connections.update(create_EX3region_connections(world))

    # Add TDM regions if enabled
    if world.options.AddTDM:
        UT_region_connections.setdefault("LadderScreen", []).append("TDM")
        UT_region_connections["TDM"] = ["TDM 1"]
        UT_region_connections.update(create_TDMregion_connections(world))

    # Create each region once and append
    created_regions: dict[str, Region] = {}
    for region_name in UT_region_connections:
        new_region = create_region(world, region_name)
        created_regions[region_name] = new_region

    # Attach map locations
    for key, data in location_table.items():
        for name, region in created_regions.items():
            if data.region == region.name:
                region.locations.append(UTLocation(world.player, key, data.id, region))

    # Attach map item locations up to the item-per-map limit
    for name, region in created_regions.items():
        count = 0
        for key, data in Map_locations.items():
            if data.region != region.name:
                continue

            if count >= world.options.RandomItemsPerMap.value:
                break

            region.locations.append(UTLocation(world.player, key, data.id, region))
            count += 1

    # Attach ladder completion locations manually because sanity?
    ladder_comp = create_Ladder_Completions(world)
    for loc_name, data in ladder_comp.items():
        for name, region in created_regions.items():
            if data.region == region.name and loc_name not in world.multiworld.regions.location_cache:
                region.locations.append(UTLocation(world.player, loc_name, data.id, region))

    return created_regions


def create_all_regions_and_connections(world: "UT99World") -> None:
    UT_region_connections.update(create_ASregion_connections(world))
    UT_region_connections.update(create_DMregion_connections(world))
    UT_region_connections.update(create_CTFregion_connections(world))
    UT_region_connections.update(create_DOMregion_connections(world))
    regions = create_regions(world)
    create_connections(world.player, regions)
    world.multiworld.regions += regions.values()


# An "Entrance" is really just a connection between two regions
def create_entrance(player: int, source: str, destination: str, regions: dict[str, Region]) -> Entrance:
    entrance = Entrance(player, f"From {source} To {destination}", regions[source])
    entrance.connect(regions[destination])
    return entrance


def create_connections(player: int, regions: dict[str, Region]) -> None:
    for source, destinations in UT_region_connections.items():
        if destinations is not None:
            new_entrances = [create_entrance(player, source, destination, regions) for destination in destinations]
            regions[source].exits = new_entrances
