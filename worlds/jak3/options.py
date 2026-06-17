from dataclasses import dataclass
from functools import cached_property
from Options import PerGameCommonOptions, StartInventoryPool, Choice, Range, OptionCounter
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
    option_defeat_errol_in_factory = 50
    option_defeat_final_boss = 60
    default = 60


class NumberOfMissionsForCompletion(Range):
    """Set the number of missions to complete for the "Complete Number of Missions" completion condition."""
    display_name = "Number of Missions for Completion"
    range_start = 5
    range_end = 164
    default = 60


class PercentOfFillerItemsReplacedWithTraps(Range):
    """
    Set the percentage of filler to be replaced with traps. This does not affect your progressive items.

    If this value is greater than the number of filler items, then they will all be replaced with traps.
    """
    display_name = "Percent of Filler Items Replaced with Traps"
    range_start = 0
    range_end = 100
    default = 0


class TrapEffectDuration(Range):
    """
    The length of time, in seconds, that a trap will last.
    """
    display_name = "Trap Effect Duration"
    range_start = 5
    range_end = 60
    default = 30


class TrapWeights(OptionCounter):
    """
    The list of traps, and corresponding weights that will be randomly added to the item pool. A trap with a weight of
    10 is twice as likely to appear than a trap with a weight of 5. Set a trap with a weight of 0 to prevent that trap
    appearing altogether. If all weights are 0, no traps are created, overriding the value of "Percent of Filler Items
    Replaced with Traps".
    """
    display_name = "Trap Weights"
    min = 0

    # Use trap names as keys
    traps = [trap for key, trap in item_table.items() if TRAP_ID_START <= key <= TRAP_ID_END]

    default = {trap.name: 1 for trap in traps}
    valid_keys = sorted({trap.name for trap in traps})

    @cached_property
    def weighted_pair(self) -> tuple[list[str], list[int]]:
        return list(self.value.keys()), list(self.value.values())


@dataclass
class Jak3Options(PerGameCommonOptions):
    jak_3_completion_condition: CompletionCondition
    specific_mission_for_completion: SpecificMissionForCompletion
    number_of_missions_for_completion: NumberOfMissionsForCompletion
    percent_filler_replaced_with_traps: PercentOfFillerItemsReplacedWithTraps
    trap_effect_duration: TrapEffectDuration
    trap_weights: TrapWeights
    start_inventory_from_pool: StartInventoryPool
