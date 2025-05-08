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
    set_rule(world.get_entrance("AS"),
             lambda state: state.has("AS-Ladder", world.player))
    set_rule(world.get_entrance("DM"),
             lambda state: state.has("DM-Ladder", world.player))
    set_rule(world.get_entrance("TDM"),
             lambda state: state.has("TDM-Ladder", world.player))
    set_rule(world.get_entrance("CTF"),
             lambda state: state.has("CTF-Ladder", world.player))
    set_rule(world.get_entrance("DOM"),
             lambda state: state.has("DOM-Ladder", world.player))
    set_rule(world.get_entrance("Challenge"),
             lambda state: state.has("Challenge-Ladder", world.player))
    set_rule(world.get_entrance("AS"),
             lambda state: state.has("EX-Ladder", world.player))
    set_rule(world.get_entrance("EX2"),
             lambda state: state.has("EX2-Ladder", world.player))
    set_rule(world.get_entrance("EX3"),
             lambda state: state.has("EX3-Ladder", world.player))