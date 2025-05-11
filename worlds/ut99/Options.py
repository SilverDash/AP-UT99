from Options import Choice, Toggle, Range, PerGameCommonOptions, DeathLink, OptionGroup
from dataclasses import dataclass
from typing import List, Dict, Any


def create_option_groups() -> List[OptionGroup]:
    option_group_list: List[OptionGroup] = []
    for name, options in ut99_option_groups.items():
        option_group_list.append(OptionGroup(name=name, options=options))
    return option_group_list


class ProgressiveWeapons(Toggle):
    """Shuffel progressive Weapon unlocks into the pool.
    Doing this will make the game harder as you will only start with an enforcer"""
    display_name = "Progressive Weapons"
    default = False

class ProgressiveArmor(Toggle):
    """Shuffle Progressive Armor unlocks into the pool.
    You won't be allowed to pick up armor you haven't unlocked.

    Thigh-Pads Chest and ShieldBelt"""
    display_name = "Progressive Armor"
    default = False


class ProgressiveBotUpgrades(Toggle):
    """In Team Games you will be given Bot companions.
    if you turn this option on your bots will start out weaker than normal and be augemnted with upgrades"""
    display_name = "Progressive Bot Stats"
    default = False


class EndGoal(Choice):
    """The end goal required to beat the game.
    XAN: Beat Xan. The final DeathMatch game on DM-HyperBlast.
    All Ladders: Beat every single Match in every ladder.
    """
    display_name = "End Goal"
    option_XAN = 1
    option_all_ladders = 2
    default = 1

class LadderRandomizer(Choice):
    """When enabled Ladder order will be randomized.
    Works with Shuffled ladder unlocks"""
    display_name = "Ladder Shuffle"
    option_false = 0
    option_light = 1
    option_insanity = 2
    default = 0


class StartingLadder(Choice):
    """Choose your starting ladder. If you choose Random and allow for extra Ladder types they will be included in the random selection"""
    display_name = "Starting Ladder"
    option_DM = 1
    option_AS = 2
    option_DOM = 3
    option_CTF = 4
    option_TDM = 5
    default = 1


class ShuffleLadderUnlocks(Choice):
    """Shuffle the ladder unlocks themselves as items"""
    Display = "Ladder Unlocks as Items"
    option_yes = 1
    option_no = 0
    default = 0


class RandomMapsPerLadder(Choice):
    """Enable Map shuffle"""
    display_name = "Randomize Maps Per Ladder"
    option_false = 0
    option_true = 1
    default = 0


class VaryRandomMapNumber(Toggle):
    """Allow for Ladders to have a random number of maps set"""
    display_name = "Random Map Count Per Ladder"
    default = False


class ExtraLadders(Toggle):
    """Enable to add extra ladders"""
    display_name="Add Extra Ladders"
    default = False


class AddTDM(Toggle):
    """Enable to add Team Death Match to the ladder"""
    display_name = "Add Team DeathMatch"
    default = False


class ExtraLaddersNumber(Range):
    """How many extra ladders to add. This will only work if you have more than the vanilla Gamemodes"""
    display_name="Extra Ladder Count"
    range_start = 0
    range_end = 3
    default = 0


class MapsPerLadderRangeMax(Range):
    """The MAX Count of Maps you want to add to each ladder
    If you Enable Random Map Count Per Ladder it will take into account your set Min and max
    If you do NOT have enough maps to fill this Max the game will adjust"""
    Display = "Maps to add to each Ladder"
    range_start = 7
    range_end = 32
    default = 7


class RandomItemsPerMap(Range):
    """Set the ammount of items to add to each map.
    These will be placed and spawn in randomly"""
    Display = "Items per map"
    range_start = 3
    range_end = 6
    default = 3


class MapsPerAS(Range):
    """Each Gametype ladder has a set default map count
    This allows you to Change that default
    This will be ignored if you don't have "vary the map count per ladder" set"""
    Display = "Maps The AS ladder Will Have"
    range_start = 6
    range_end = 20
    default = 6


class MapsPerDM(Range):
    """Each Gametype ladder has a set default map count
    This allows you to Change that default
    This will be ignored if you don't have "vary the map count per ladder" set"""
    Display = "Maps The AS ladder Will Have"
    range_start = 14
    range_end = 20
    default = 14


class MapsPerTDM(Range):
    """Each Gametype ladder has a set default map count
    This allows you to Change that default
    This will be ignored if you don't have "vary the map count per ladder" set"""
    Display = "Maps The TDM ladder Will Have"
    range_start = 14
    range_end = 20
    default = 14


class MapsPerCTF(Range):
    """Each Gametype ladder has a set default map count
    This allows you to Change that default
    This will be ignored if you don't have "vary the map count per ladder" set"""
    Display = "Maps The CTF ladder Will Have"
    range_start = 10
    range_end = 20
    default = 10


class MapsPerDOM(Range):
    """Each Gametype ladder has a set default map count
    This allows you to Change that default
    This will be ignored if you don't have "vary the map count per ladder" set"""
    Display = "Maps The DOM ladder Will Have"
    range_start = 9
    range_end = 20
    default = 9


class MapsPerEX(Range):
    """Each Gametype ladder has a set default map count
    This allows you to Change that default
    This will be ignored if you don't have "vary the map count per ladder" set"""
    Display = "Maps The EX ladder Will Have(If enabled)"
    range_start = 7
    range_end = 20
    default = 7


class MapsPerEX2(Range):
    """Each Gametype ladder has a set default map count
    This allows you to Change that default
    This will be ignored if you don't have "vary the map count per ladder" set"""
    Display = "Maps The EX3 ladder Will Have(If enabled)"
    range_start = 7
    range_end = 20
    default = 7


class MapsPerEX3(Range):
    """Each Gametype ladder has a set default map count
    This allows you to Change that default
    This will be ignored if you don't have "vary the map count per ladder" set"""
    Display = "Maps The EX3 ladder Will Have(If enabled)"
    range_start = 7
    range_end = 20
    default = 7


class CustomMapRanges(Toggle):
    """Set this if you want to manually set your map counts per ladder"""
    Display = "Enable Manual Map Count Ranges"
    default = False


@dataclass
class UTOptions(PerGameCommonOptions):
    prog_armor: ProgressiveArmor
    prog_weapons: ProgressiveWeapons
    prog_Bots: ProgressiveBotUpgrades

    EndGoal: EndGoal

    RandomMapsPerLadder:RandomMapsPerLadder
    VaryRandomMapNumber:VaryRandomMapNumber
    ShuffleLadderUnlocks:ShuffleLadderUnlocks
    MapsPerLadderRangeMax:MapsPerLadderRangeMax
    StartingLadder:StartingLadder
    LadderRandomizer:LadderRandomizer
    ExtraLadders:ExtraLadders
    ExtraLaddersNumber:ExtraLaddersNumber
    RandomItemsPerMap:RandomItemsPerMap
    CustomMapRanges:CustomMapRanges
    MapsPerAS:MapsPerAS
    MapsPerDM:MapsPerDM
    MapsPerTDM:MapsPerTDM
    MapsPerDOM:MapsPerDOM
    MapsPerCTF:MapsPerCTF
    MapsPerEX:MapsPerEX
    MapsPerEX2:MapsPerEX2
    MapsPerEX3:MapsPerEX3
    AddTDM:AddTDM



    death_link: DeathLink


ut99_option_groups: Dict[str, List[Any]] = {
    "General Options":[EndGoal, ShuffleLadderUnlocks],

    "LadderOptions":[AddTDM, RandomMapsPerLadder,ExtraLadders,ExtraLaddersNumber,StartingLadder,LadderRandomizer],
    "Map Options": [MapsPerLadderRangeMax, CustomMapRanges,VaryRandomMapNumber,MapsPerAS,MapsPerDM,MapsPerDOM,MapsPerCTF,MapsPerTDM,MapsPerEX,MapsPerEX2,MapsPerEX3],
    "Item Options": [ProgressiveBotUpgrades,ProgressiveArmor,ProgressiveWeapons,RandomItemsPerMap]

}