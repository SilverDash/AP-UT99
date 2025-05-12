from BaseClasses import Item, Tutorial, MultiWorld
from Options import OptionError
from worlds.AutoWorld import WebWorld, World
from typing import Dict, Any
from . import Items, Locations, Regions, Rules
from .Items import g_item_table, create_item,victory_item
from .Options import UTOptions, RandomItemsPerMap,ExtraLadders,CustomMapRanges,ExtraLaddersNumber,VaryRandomMapNumber,MapsPerAS,MapsPerCTF,MapsPerDM,MapsPerDOM,MapsPerEX,MapsPerEX2,MapsPerEX3,MapsPerTDM

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
    Unreal Tournament is a FirstPerson Arena Shooter developed by Epic Mega Games back in 1999.
    Initially an expansion pack for Unreal 1998 it became its own game after some development time.

    You'll participate in a multitude of matches of game modes to win the tournament.
    """
    game = "Unreal Tournament"
    options: UTOptions
    options_dataclass = UTOptions

    item_name_to_id = {name: data.code for name, data in g_item_table.items()}
    location_name_to_id = Locations.get_loc_names()

    web = UT99Web()
    # and there was a better way. Thanks medic
    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)
        self.TDMRange = range(MapsPerTDM.default)
        self.DMRange = range(MapsPerDM.default)
        self.ASRange = range(MapsPerAS.default)
        self.DOMRange = range(MapsPerDOM.default)
        self.CTFRange = range(MapsPerCTF.default)
        self.EXRange = range(MapsPerEX.default)
        self.EX2Range = range(MapsPerEX2.default)
        self.EX3Range = range(MapsPerEX3.default)


    def generate_early(self):
        if not self.multiworld.get_player_name(self.player).isascii():
            raise OptionError("UT99 yaml's slot name has invalid character(s).")
        Regions.set_mapranges(self)


    def create_regions(self):
        Regions.create_all_regions_and_connections(self)
        self.multiworld.get_location("CHALLANGE Map 4 Completion",self.player).place_locked_item(create_item(self, "Victory"))

        if not self.options.ShuffleLadderUnlocks:
            for loc_name, loc_data in Ladder_Completions.items():
                loc = self.get_location(loc_name)
                for item_name in loc_data.required_ladderItem:
                    item = create_item(self, item_name)
                    loc.place_locked_item(item)

    def create_items(self):
        Items.create_all_items(self)

    def set_rules(self):
        Rules.set_rules(self)

    def create_item(self, name: str) -> Item:
        return Items.create_item(self, name)

    # Lots to send to the client
    def fill_slot_data(self) -> Dict[str, Any]:
        return self.options.as_dict("death_link","EndGoal","prog_armor","prog_weapons",
                                    "prog_Bots","RandomMapsPerLadder","VaryRandomMapNumber","ExtraLaddersNumber",
                                    "ShuffleLadderUnlocks","StartingLadder","LadderRandomizer","ExtraLadders",
                                    "RandomItemsPerMap","CustomMapRanges","MapsPerAS","MapsPerDM","MapsPerTDM",
                                    "MapsPerDOM","MapsPerCTF","MapsPerEX","MapsPerEX2","MapsPerEX3")
