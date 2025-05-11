from typing import NamedTuple,TYPE_CHECKING
from BaseClasses import CollectionState
from worlds.generic.Rules import set_rule


if TYPE_CHECKING:
    from . import UT99World

class EntranceLock(NamedTuple):
    source: str
    destination: str
    event: str
    items_needed: int

def has_beaten(world: "UT99World",state: CollectionState, loc: str) -> bool:
    for check in state.locations_checked:
        return bool(check == loc)
    else:
        return False

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
        set_rule(loc,lambda state: state.has("AS-Ladder", world.player))
    if world.options.AddTDM:
        for loc in world.get_region("TDM").locations:
            set_rule(loc,lambda state: state.has("TDM-Ladder", world.player))
    if world.options.ExtraLadders:
        for loc in world.get_region("EX").locations:
            set_rule(loc,lambda state: state.has("EX-Ladder", world.player))
        for loc in world.get_region("EX2").locations:
            set_rule(loc,lambda state: state.has("EX2-Ladder", world.player))
        for loc in world.get_region("EX3").locations:
            set_rule(loc,lambda state: state.has("EX3-Ladder", world.player))