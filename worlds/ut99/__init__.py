from BaseClasses import Item, Tutorial, MultiWorld
from Options import OptionError
from worlds.AutoWorld import WebWorld, World
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
        tutorial_name="MutliWorld Setup Guide",
        description="A guide to setting up your UnrealTournament game for Archipelago MultiWorld games.",
        language="English",
        file_name="setup_en.md",
        link="setup/en",
        authors=["SnowySilver"]
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
    TDMRange: range
    DMRange: range
    ASRange: range
    DOMRange: range
    CTFRange: range
    EXRange: range
    EX2Range: range
    EX3Range: range

    web = UT99Web()
    # and there was a better way. Thanks medic
    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)


    def generate_early(self):
        if not self.multiworld.get_player_name(self.player).isascii():
            raise OptionError("UT99 yaml's slot name has invalid character(s).")
        self.TDMRange = range(self.options.MapsPerTDM.value+1)
        self.DMRange = range(self.options.MapsPerDM.value+1)
        self.ASRange = range(self.options.MapsPerAS.value+1)
        self.DOMRange = range(self.options.MapsPerDOM.value+1)
        self.CTFRange = range(self.options.MapsPerCTF.value+1)
        self.EXRange = range(self.options.MapsPerEX.value+1)
        self.EX2Range = range(self.options.MapsPerEX2.value+1)
        self.EX3Range = range(self.options.MapsPerEX3.value+1)
        Regions.set_mapranges(self)


    def create_regions(self):
        Regions.create_all_regions_and_connections(self)
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
        self.multiworld.get_location("CHALLANGE Map 4 Completion",self.player).place_locked_item(
            create_item(self, "Victory"))
        self.multiworld.get_location("CHALLANGE Map 3 Completion",self.player).place_locked_item(
            create_item(self, "Challange-Ladder"))
        self.multiworld.get_location("CHALLANGE Map 2 Completion",self.player).place_locked_item(
            create_item(self, "Challange-Ladder"))
        self.multiworld.get_location("CHALLANGE Map 1 Completion",self.player).place_locked_item(
            create_item(self, "Challange-Ladder"))
        if not self.options.ShuffleLadderUnlocks:
            self.multiworld.get_location("Ladder Completion (DM)", self.player).place_locked_item(
                create_item(self, "DOM-Ladder"))
            self.multiworld.get_location("Ladder Completion (DOM)", self.player).place_locked_item(
                create_item(self, "CTF-Ladder"))
            self.multiworld.get_location("Ladder Completion (CTF)", self.player).place_locked_item(
                create_item(self, "AS-Ladder"))
            self.multiworld.get_location("Ladder Completion (AS)", self.player).place_locked_item(
                create_item(self, "Challange-Ladder"))
            if self.options.AddTDM:
                self.multiworld.get_location("Ladder Completion (DM) - (TDM Unlock)", self.player).place_locked_item(
                    create_item(self, "TDM-Ladder"))
            if self.options.ExtraLadders:
                self.multiworld.get_location("Ladder Completion (EX)", self.player).place_locked_item(
                    create_item(self, "EX-Ladder"))
                self.multiworld.get_location("Ladder Completion (EX2)", self.player).place_locked_item(
                    create_item(self, "EX-Ladder"))
                self.multiworld.get_location("Ladder Completion (EX3)", self.player).place_locked_item(
                    create_item(self, "EX-Ladder"))


    def create_items(self):
        Items.create_all_items(self)

    def get_filler_item_name(self) -> str:
        return self.random.choice(["Random-Goodie", "Trap"])

    def set_rules(self):
        Rules.set_rules(self)
        Rules.make_plot(self)

    def create_item(self, name: str) -> Item:
        return Items.create_item(self, name)

    # Lots to send to the client
    def fill_slot_data(self) -> dict[str, any]:
        return self.options.as_dict("death_link","EndGoal","prog_armor","prog_weapons",
                                    "prog_Bots","RandomMapsPerLadder","VaryRandomMapNumber","ExtraLaddersNumber",
                                    "ShuffleLadderUnlocks","StartingLadder","LadderRandomizer","ExtraLadders",
                                    "RandomItemsPerMap","CustomMapRanges","MapsPerAS","MapsPerDM","MapsPerTDM",
                                    "MapsPerDOM","MapsPerCTF","MapsPerEX","MapsPerEX2","MapsPerEX3","AddTDM")
