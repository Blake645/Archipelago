# Archipelago Imports
import settings
from Options import OptionError, OptionGroup
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import components, Component, launch_subprocess, Type, icon_paths
from BaseClasses import (Tutorial, ItemClassification as ItemClass)
from typing import cast, ClassVar, Any

# Jak 3 imports
from . import options
from .game_id import jak3_name, jak3_max
from .items import (item_table, ITEM_ID_KEY_START, ITEM_ID_KEY_END, ITEM_ID_FILLER_START, ITEM_ID_FILLER_END,
                    TRAP_ID_START, TRAP_ID_END, Jak3ItemData, Jak3Item)
from .locs import (mission_locations)
from .locations import (Jak3Location, all_locations_table)
from .locs.mission_locations import Jak3MissionData
from .regs.region_base import Jak3Region


class Jak3Settings(settings.Group):
    class RootDirectory(settings.UserFolderPath):
        """Path to folder containing the ArchipelagoGOAL Jak 3 mod executables (gk.exe and goalc.exe).
        Ensure this path contains forward slashes (/) only. This setting only applies if
        Auto Detect Root Directory is set to false."""
        description = "ArchipelagoGOAL Jak 3 Root Directory"

    class AutoDetectRootDirectory(settings.Bool):
        """Attempt to find the OpenGOAL installation and the Jak 3 mod executables (gk.exe and goalc.exe)
        automatically. If set to true, the ArchipelaGOAL Jak 3 Root Directory setting is ignored."""
        description = "ArchipelagoGOAL Jak 3 Auto Detect Root Directory"

    root_directory: RootDirectory = "C:/Program Files/OpenGOAL/features/jak3/mods/archipelagoal/archipelagoal"
    auto_detect_root_directory: AutoDetectRootDirectory = True


def launch_client():
    from . import client
    launch_subprocess(client.launch, name="Jak3Client")


components.append(Component("Jak 3 Client",
                            func=launch_client,
                            component_type=Type.CLIENT,
                            icon="jak3_icon"))


# TODO: Add proper icon for Jak 3
icon_paths["jak3_icon"] = f"ap:{__name__}/icons/jak3_icon.png"


class Jak3WebWorld(WebWorld):
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up ArchipelagoGOAL 3 (Archipelago on OpenGOAL)",
        "English",
        "setup_en.md",
        "setup/en",
        ["Blake645"]
    )

    tutorials = [setup_en]
    bug_report_page = "https://github.com/Blake645/Archipelago/issues"
    #option_groups = [
        #OptionGroup("Traps", [
        #    options.PercentOfFillerItemsReplacedWithTraps,
        #    options.TrapEffectDuration,
        #    options.TrapWeights
        #])
    #]


class Jak3World(World):
    """
Jak 3 is a 2004 action-adventure platformer video game developed by Naughty Dog and published by Sony Computer Entertainment
for the PlayStation 2 (PS2). The game is the sequel to Jak II (2003) and serves as the conclusion of the trilogy.
The story of the previous games continues as the player takes on the dual role of recurring protagonists Jak and Daxter.
It adds new weapons, devices and playable areas.
    """

    game = jak3_name
    web = Jak3WebWorld()

    # Options
    options_dataclass = options.Jak3Options
    options: options.Jak3Options

    # Settings will be applied after class definition
    settings: ClassVar[Jak3Settings]

    item_name_to_id = {item_data.name: k for k, item_data in item_table.items()}
    location_name_to_id = {data.name: k for k, data in all_locations_table.items()}
    item_name_groups = {
        "Items": {item.name for item in item_table.values()}
    }
    location_name_groups = {}
    origin_region_name = "Mission Tree"

    # Cache option-related values.
    completion_type: int
    completion_value: int
    total_items: int = 56
    total_prog_items: int = 33
    total_filler_items: int = 0
    total_trap_items: int = 0
    trap_weights: tuple[list[str], list[int]]

    def generate_early(self) -> None:
        # Cache completion conditions and values.
        self.completion_type = self.options.jak_3_completion_condition.value  # Sorry about the naming here.
        if self.completion_type == options.CompletionCondition.option_complete_specific_mission:
            self.completion_value = self.options.specific_mission_for_completion.value
        elif self.completion_type == options.CompletionCondition.option_complete_number_of_missions:
            self.completion_value = self.options.number_of_missions_for_completion.value
        else:
            raise OptionError(f"Unknown completion condition selected for Jak 3: {self.completion_type}")

        # Calculate Filler and Traps, if applicable
        #if self.options.percent_filler_replaced_with_traps > 0:
        #    self.total_trap_items = (
        #        int((
        #            self.options.percent_filler_replaced_with_traps / 100) * (self.total_items - self.total_prog_items))
        #        )
        #    self.total_filler_items = self.total_items - self.total_prog_items - self.total_trap_items

       # self.trap_weights = self.options.trap_weights.weighted_pair

    @staticmethod
    def item_data_helper(item: int) -> list[tuple[int, ItemClass, int]]:
        # count,num,classification
        data: list[tuple[int, ItemClass, int]] = []

        # Determine item classification based on ID ranges
        if ITEM_ID_KEY_START <= item <= ITEM_ID_KEY_END:
            # Key/progression items (IDs 1-33)
            data.append((1, ItemClass.progression | ItemClass.useful, 0))
        elif ITEM_ID_FILLER_START <= item <= ITEM_ID_FILLER_END:
            # Filler items (IDs 34-39) (will be made manually)
            data.append((0, ItemClass.filler, 0))
        elif TRAP_ID_START <= item <= TRAP_ID_END:
            # Trap Items (their own table) (will also be made manually)
            data.append((0, ItemClass.trap, 0))
        else:
            # If we try to make items with ID's outside defined ranges, something has gone wrong
            raise KeyError(f"Tried to fill item pool with unknown ID {item}. Valid ranges: "
                           f"key items ({ITEM_ID_KEY_START}-{ITEM_ID_KEY_END}), "
                           f"filler items ({ITEM_ID_FILLER_START}-{ITEM_ID_FILLER_END})"
                           f"trap items ({TRAP_ID_START}-{TRAP_ID_END})")
        return data

    def create_items(self) -> None:
        items_made: int = 0
        for item_name in self.item_name_to_id:
            item_id = self.item_name_to_id[item_name]

            data = self.item_data_helper(item_id)
            for (count, classification, num) in data:
                self.multiworld.itempool += [
                    Jak3Item(item_name, classification, item_id, self.player)
                    for _ in range(count)]
                items_made += 1

            # Skip traps
            if TRAP_ID_START <= item_id <= TRAP_ID_END:
                continue

        all_regions = self.multiworld.get_regions(self.player)
        total_locations = sum(reg.location_count for reg in cast(list[Jak3Region], all_regions))
        total_filler = total_locations - items_made
        self.multiworld.itempool += [self.create_filler() for _ in range(total_filler)]

        # Handle Traps (fr!!)
        # Manually filling the item pool with an assortment of traps. Only done if one or more traps have a weight > 0.
        #names, weights = self.trap_weights
        #if sum(weights):
        #    total_traps = self.total_trap_items
        #    trap_list = self.random.choices(names, weights=weights, k=total_traps)
        #    self.multiworld.itempool += [self.create_item(trap_name) for trap_name in trap_list]
        #    items_made += total_traps

        # Handle Unfilled Locations!
        all_regions = self.multiworld.get_regions(self.player)
        total_locations = sum(reg.location_count for reg in cast(list[Jak3Region], all_regions))
        total_filler = total_locations - items_made
        self.multiworld.itempool += [self.create_filler() for _ in range(total_filler)]

    def create_item(self, name: str) -> Jak3Item:
        item_id = self.item_name_to_id[name]

        _, classification, _ = self.item_data_helper(item_id)[0]
        return Jak3Item(name, classification, item_id, self.player)

    def get_filler_item_name(self) -> str:
        filler_item_names = ["Dark Eco Pill", "Light Eco Pill", "Skull Gems", "Health Pack", "Scatter Gun Ammo", "Blaster Ammo", "Vulcan Fury Ammo",
                             "Peacemaker Ammo"]
        return self.random.choice(filler_item_names)

    def create_regions(self) -> None:

        # Add missions to the mission tree.
        mission_tree_region = Jak3Region("Mission Tree", self.player, self.multiworld)
        for mission_id in all_locations_table:
            mission = all_locations_table[mission_id]
            mission_tree_region.add_jak_mission(mission_id, mission.name, mission.rule)

        self.multiworld.regions.append(mission_tree_region)

        # Handle completion condition.
        if self.completion_type == options.CompletionCondition.option_complete_specific_mission:
            mission = all_locations_table[self.completion_value]

            self.multiworld.completion_condition[self.player] = lambda state: (
                state.can_reach_location(mission.name, player=self.player))

        elif self.completion_type == options.CompletionCondition.option_complete_number_of_missions:
            def _completion_rule(state, player) -> bool:
                completed_count = 0
                for _, miss in all_locations_table.items():
                    if miss.rule(state, player):
                        completed_count += 1
                return completed_count >= self.completion_value

            self.multiworld.completion_condition[self.player] = lambda state: (
                _completion_rule(state=state, player=self.player))

    def fill_slot_data(self) -> dict[str, Any]:
        options_dict = self.options.as_dict("jak_3_completion_condition",
                                            "specific_mission_for_completion",
                                            "number_of_missions_for_completion",
                                            #"percent_filler_replaced_with_traps",
                                            #"trap_effect_duration",
                                            #"trap_weights",
                                            )
        return options_dict
