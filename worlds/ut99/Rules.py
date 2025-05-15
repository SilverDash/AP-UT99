from typing import NamedTuple,TYPE_CHECKING
from BaseClasses import CollectionState,Region
from worlds.generic.Rules import set_rule
from .Items import ladder_items
from .Locations import Ladder_Completions


if TYPE_CHECKING:
    from . import UT99World, Ladder_Completions


class EntranceLock(NamedTuple):
    source: str
    destination: str
    event: str
    items_needed: int


def has_beaten_all_ladders(world: "UT99World",state: CollectionState) -> bool:
    for _, data in Ladder_Completions.items():
        reg = world.get_region(data.region)
        if not reg.can_reach(state):
            return False
    return True

def has_EXwin_count(state: CollectionState, player: int, amount: int) -> bool:
    return state.count("EX-Ladder", player) >= amount

def has_ladder_win_count(state: CollectionState, player: int, amount: int, ladder_item: str) -> bool:
    return state.count(ladder_item, player) >= amount

def set_rules(world: "UT99World"):
    for loc in world.get_region("AS").locations:
        set_rule(loc,lambda state: state.has("AS-Ladder", world.player))
    for loc in world.get_region("DM").locations:
        set_rule(loc,lambda state: state.has("DM-Ladder", world.player))
    for loc in world.get_region("DOM").locations:
        set_rule(loc,lambda state: state.has("DOM-Ladder", world.player))
    for loc in world.get_region("CTF").locations:
        set_rule(loc,lambda state: state.has("CTF-Ladder", world.player))
    for loc in world.get_region("Challenge").locations:
        set_rule(loc,lambda state: has_beaten_all_ladders(world,state))
    for loc in world.get_region("Challenge 1").locations:
        set_rule(loc,lambda state: has_beaten_all_ladders(world,state)and has_ladder_win_count(state, world.player, 1, "Challange-Ladder"))
    for loc in world.get_region("Challenge 2").locations:
        set_rule(loc,lambda state: has_beaten_all_ladders(world,state) and has_ladder_win_count(state, world.player, 2, "Challange-Ladder"))
    for loc in world.get_region("Challenge 3").locations:
        set_rule(loc,lambda state: has_beaten_all_ladders(world,state) and has_ladder_win_count(state, world.player, 3, "Challange-Ladder"))
    if world.options.AddTDM:
        for loc in world.get_region("TDM").locations:
            set_rule(loc,lambda state: state.has("TDM-Ladder", world.player))
    if world.options.ExtraLadders:
        for loc in world.get_region("EX").locations:
            set_rule(loc,lambda state: has_EXwin_count(state, world.player,1))
        for loc in world.get_region("EX2").locations:
            set_rule(loc,lambda state: has_EXwin_count(state, world.player,2))
        for loc in world.get_region("EX3").locations:
            set_rule(loc,lambda state: has_EXwin_count(state, world.player,3))


from Utils import visualize_regions
def make_plot(world:"UT99World"):
    visualize_regions(world.multiworld.get_region("Menu",world.player),"UT99_world.puml")