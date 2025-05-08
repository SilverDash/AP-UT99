from BaseClasses import Item, ItemClassification, Tutorial, Location, MultiWorld
from worlds.AutoWorld import WebWorld, World
from typing import Dict, Any
from . import Events, Items, Locations, Regions, Rules
from .Items import item_table, create_item
from .Options import UTOptions
from .Locations import location_table ,Ladder_Completions
from worlds.LauncherComponents import Component, components, icon_paths, launch as launch_component, Type
from Utils import local_path
from .Regions import create_regions


def launch_client():
    from .Client import launch
    launch_component(launch, name="UTClient")

components.append(Component("Unreal Tournament Client", "UTClient", func=launch_client,
                            component_type=Type.CLIENT, icon='UT99'))

icon_paths['UT99'] = local_path('data', 'UT99.png')



class UT99Web(WebWorld):
    tutorials = [Tutorial(
        "MutliWorld Setup Guide",
        "A guide to setting up your UnrealTournament game for Archipelago MultiWorld games.",
        "English",
        "setup_en.md",
        "setup/en",
        ["SnowySilver"]
    )]
    theme = "stone"
    bug_report_page = "https://github.com/SilverDash/AP-UT99/issues"


class UT99World(World):
    """
    Unreal Tournament is a FirstPerson Arena Shooter developed by epic games back in 1999.
    Initially an expansion pack for Unreal 1998 it became its own game after some development time.

    You'll participate in a multitude of matches of game modes to win the tournament.
    """
    game = "Unreal Tournament"
    options = UTOptions
    options_dataclass = UTOptions

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = Locations.get_loc_names()

    web = UT99Web()

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)


    def generate_early(self):
        Regions.set_mapranges()
        if not self.multiworld.get_player_name(self.player).isascii():
            raise Exception("UT99 yaml's slot name has invalid character(s).")

    def create_regions(self):
        Regions.create_regions(self)
        if not self.options.ShuffleLadderUnlocks:
            for name in Ladder_Completions.keys():
                loc = self.get_location(name)
                loc.place_locked_item(create_item(self, name))

    def create_items(self):
        Items.create_all_items(self)

    def set_rules(self):
        Rules.set_rules(self)

    def create_item(self, name: str) -> Item:
        return Items.create_item(self, name)

    # Lots to send to the client
    def fill_slot_data(self) -> Dict[str, Any]:
        return self.Options.as_dict("death_link","EndGoal","prog_armor","prog_weapons",
                                    "prog_Bots","RandomMapsPerLadder","VaryRandomMapNumber","ExtraLaddersNumber",
                                    "ShuffleLadderUnlocks","StartingLadder","LadderRandomizer","ExtraLadders",
                                    "RandomItemsPerMap","CustomMapRanges","MapsPerAS","MapsPerDM","MapsPerTDM",
                                    "MapsPerDOM","MapsPerCTF","MapsPerEX","MapsPerEX2","MapsPerEX3")
