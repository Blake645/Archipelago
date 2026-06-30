from dataclasses import dataclass
from functools import cached_property
from Options import PerGameCommonOptions, StartInventoryPool, Choice, Range, Toggle, OptionCounter
from .items import item_table, TRAP_ID_START, TRAP_ID_END

class CompletionCondition(Choice):
    """Set your goal for completion!"""
    display_name = "Completion Condition"
    option_complete_specific_mission = 1
    option_complete_number_of_missions = 2
    default = 1

class SpecificMissionForCompletion(Choice):
    """Set the specific mission to complete for the "Complete Specific Mission" completion condition."""
    display_name = "Specific Mission for Completion"
    option_defeat_robot_in_mines = 25
    option_defeat_errol_in_factory = 60
    option_defeat_final_boss = 71
    default = 71

class NumberOfMissionsForCompletion(Range):
    """Set the number of missions to complete for the "Complete Number of Missions" completion condition."""
    display_name = "Number of Missions for Completion"
    range_start = 5
    range_end = 164
    default = 60

class ChecksPerMission(Range):
    """Set the number of Archipelago checks each mission gives."""
    display_name = "Checks Per Mission"
    range_start = 1
    range_end = 10
    default = 5

class JakIsJak2(Toggle):
    """Changes Jak's model to his Jak II appearance. WARNING: Shadows are a bit broken, and you won't see things like armor on Jak."""
    display_name = "Jak is Jak 2"

@dataclass
class Jak3Options(PerGameCommonOptions):
    jak_3_completion_condition: CompletionCondition
    specific_mission_for_completion: SpecificMissionForCompletion
    number_of_missions_for_completion: NumberOfMissionsForCompletion
    checks_per_mission: ChecksPerMission
    jak_is_jak2: JakIsJak2
    start_inventory_from_pool: StartInventoryPool