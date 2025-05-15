from BaseClasses import Item, ItemClassification
from .Types import ItemData, UTItem
from typing import List, Dict, TYPE_CHECKING


if TYPE_CHECKING:
    from . import UT99World


ladder_items:Dict[str, ItemData] ={
    "AS-Ladder":ItemData(1,ItemClassification.progression),
    "DM-Ladder":ItemData(2,ItemClassification.progression),

    "CTF-Ladder":ItemData(4,ItemClassification.progression_skip_balancing),
    "DOM-Ladder":ItemData(5,ItemClassification.progression_skip_balancing),
    "Challange-Ladder":ItemData(6,ItemClassification.progression_skip_balancing)
}


victory_item={"Victory":ItemData(42069,ItemClassification.progression)}


ex_ladder_items:Dict[str,ItemData]={
    "Extra-Ladder":ItemData(7,ItemClassification.progression)
}


prog_items:Dict[str, ItemData]={
    "Progressive-Weapons": ItemData(100, ItemClassification.useful),
    "Progressive-Armor": ItemData(200, ItemClassification.useful),
    "Progressive-BotUpgrade": ItemData(300, ItemClassification.useful),
}


item_table:Dict[str, ItemData]={
    "Random-Goodie": ItemData(400,ItemClassification.filler),
    "Translocator": ItemData(150, ItemClassification.useful),
    "Trap": ItemData(500,ItemClassification.trap)
}

tdm_ladder_unlock:Dict[str,ItemData]={"TDM-Ladder":ItemData(3,ItemClassification.progression)}

g_item_table = {
    **prog_items,
    **ladder_items,
    **ex_ladder_items,
    **item_table,
    **victory_item,
    **tdm_ladder_unlock
}


def create_item(world: "UT99World", name: str) -> Item:
    data = g_item_table[name]
    return UTItem(name, data.classification, data.code, world.player)


def create_all_items(world: "UT99World") -> None:
    player = world.player
    ExCount = world.options.ExtraLaddersNumber.value
    locations_to_fill = len(world.multiworld.get_unfilled_locations(player))
    itempool:List[str]=[]

    #itempool += item_table

    # Create the ladders if set
    if world.options.ShuffleLadderUnlocks:
        itempool += ladder_items
        if ExCount > 0:
            itempool += create_extra_ladder_items(ExCount)
        if world.options.AddTDM:
            itempool += {"TDM-Ladder":ItemData(3,ItemClassification.progression)}

    if world.options.prog_armor:
        itempool += create_progressives(3,"Progressive-Armor")

    if world.options.prog_Bots:
        itempool += create_progressives(8, "Progressive-BotUpgrade")

    if world.options.prog_weapons:
        itempool += create_progressives(9, "Progressive-Weapons")

    itempool += create_random_items(world,locations_to_fill)

    world.multiworld.itempool += [create_item(world,name) for name in itempool]


def create_extra_ladder_items(count:int)->list[str]:
    return ["Extra-Ladder" for _ in range(count)]


def create_progressives(count:int,name:str)->list[str]:
    return [name for _ in range(count)]


def create_random_items(world: "UT99World", count:int)->list[str]:
    filler_pool = {"Random-Goodie":70,"Trap":30}
    return world.random.choices(population=list(filler_pool.keys()),
                                weights=list(filler_pool.values()),
                                k=count)

