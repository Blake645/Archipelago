from typing import Callable, Optional
from worlds.jak3.rules import (spargus_to_desert, spargus_to_monk_temple, spargus_to_nest, spargus_to_port, port_to_metal_head_section,
port_to_inda, port_to_indb, port_to_hq, port_to_ruins, any_gun, car_with_guns)
from worlds.stardew_valley.stardew_rule import state


class Jak3MissionData:
    mission_id: int  # Mission ID is how Archipelago identifies the location.
    task_id: int  # Task ID is how GOAL identifies the location.
    name: str
    rule: Callable

    def __init__(self, mission_id: int, task_id: int, name: str, rule: Optional[Callable] = None):
        self.mission_id = mission_id
        self.task_id = task_id
        self.name = name
        if rule:
            self.rule = rule
        else:
            self.rule = lambda state, player: True


class Jak3SideMissionData:
    mission_id: int  # Mission ID is how Archipelago identifies the location.
    task_id: int  # Task ID is how GOAL identifies the location.
    name: str
    rule: Callable

    def __init__(self, mission_id: int, task_id: int, name: str, rule: Optional[Callable] = None):
        self.mission_id = mission_id
        self.task_id = task_id
        self.name = name
        if rule:
            self.rule = rule
        else:
            self.rule = lambda state, player: True


# Names for Missions are taken directly from the game
main_mission_table = {
    # Act 1
    1: Jak3MissionData(mission_id=1, task_id=10, name="Complete arena training course"),
    2: Jak3MissionData(mission_id=2, task_id=11, name="Earn 1st war amulet"),
    3: Jak3MissionData(mission_id=3, task_id=12, name="Catch kanga-rats"),
    4: Jak3MissionData(mission_id=4, task_id=13, name="Unlock satellite"),
    5: Jak3MissionData(mission_id=5, task_id=14, name="Learn to Drive Vehicle",
                       rule=lambda state, player:
                       state.has_all(("Gate Pass to Spargus", "Tough Puppy"), player)),
    6: Jak3MissionData(mission_id=6, task_id=15, name="Beat Kleiver in desert race",
                       rule=lambda state, player:
                       state.has_all(("Gate Pass to Spargus", "Tough Puppy"), player)),
    7: Jak3MissionData(mission_id=7, task_id=16, name="Race for artifacts",
                       rule=lambda state, player:
                       state.has_all(("Gate Pass to Spargus", "Tough Puppy"), player)),
    8: Jak3MissionData(mission_id=8, task_id=17, name="Beat monks in leaper race"),
    9: Jak3MissionData(mission_id=9, task_id=18, name="Destroy metal head beasts",
                       rule=lambda state, player:
                       state.has_all(("Gate Pass to Spargus", "Sand Shark"), player)),
    10: Jak3MissionData(mission_id=10, task_id=19, name="Earn 2nd war amulet"),
    11: Jak3MissionData(mission_id=11, task_id=20, name="Corral wild leapers",
                        rule=lambda state, player:
                        state.has_all(("Gate Pass to Spargus", "Sand Shark"), player)),
    12: Jak3MissionData(mission_id=12, task_id=21, name="Rescue wastelanders",
                        rule=lambda state, player:
                        state.has_all(("Gate Pass to Spargus", "Sand Shark"), player)),
    13: Jak3MissionData(mission_id=13, task_id=22, name="Beat turret challenge",
                        rule=lambda state, player:
                        state.has("Gun Turret", player)),
    14: Jak3MissionData(mission_id=14, task_id=23, name="Defeat marauders in arena",
                        rule=lambda state, player:
                        any_gun(state, player)),
    15: Jak3MissionData(mission_id=15, task_id=24, name="Destroy eggs in nest",
                        rule=lambda state, player:
                        spargus_to_nest(state, player)),
    16: Jak3MissionData(mission_id=16, task_id=25, name="Climb Monk Temple tower",
                        rule=lambda state, player:
                        spargus_to_monk_temple(state, player)),
    17: Jak3MissionData(mission_id=17, task_id=26, name="Glide to volcano",
                        rule=lambda state, player:
                        spargus_to_monk_temple(state, player)
                        and state.has_any("Blaster", "Beam Reflexor", "Vulcan Fury", "Arc Wielder", "Needle Lazer")),
    18: Jak3MissionData(mission_id=18, task_id=27, name="Find satellite in volcano",
                        rule=lambda state, player:
                        spargus_to_monk_temple(state, player)
                        and any_gun(state, player)),
    19: Jak3MissionData(mission_id=19, task_id=28, name="Find oracle in Monk Temple",
                        rule=lambda state, player:
                        spargus_to_monk_temple(state, player)
                        and state.has_all("Wave Concussor", "Dark Invisibility", player)),
    20: Jak3MissionData(mission_id=20, task_id=29, name="Defend Ashelin at oasis",
                        rule=lambda state, player:
                        spargus_to_desert(state, player)
                        and any_gun(state, player)),
    21: Jak3MissionData(mission_id=21, task_id=30, name="Complete Monk Temple tests",
                        rule=lambda state, player:
                        spargus_to_monk_temple(state, player)
                        and state.has_all("Seal of Mar", "JET-Board", "Light Jak" "Light Flash Freeze", player)),
    22: Jak3MissionData(mission_id=22, task_id=31, name="Travel through catacomb subrails",
                        rule=lambda state, player:
                        spargus_to_monk_temple(state, player)
                        and state.has_all("Seal of Mar", "JET-Board", "Light Jak" "Light Flash Freeze", player)),
    23: Jak3MissionData(mission_id=23, task_id=32, name="Explore eco mine",
                        rule=lambda state, player:
                        spargus_to_monk_temple(state, player)
                        and state.has("JET-Board", player)
                        and state.has_any("Blaster", "Beam Reflexor", "Vulcan Fury", "Arc Wielder", "Needle Lazer")),
    24: Jak3MissionData(mission_id=24, task_id=33, name="Escort bomb train",
                        rule=lambda state, player:
                        spargus_to_monk_temple(state, player)
                        and state.has("JET-Board", player)
                        and state.has_any("Blaster", "Beam Reflexor", "Vulcan Fury", "Arc Wielder", "Needle Lazer")),
    25: Jak3MissionData(mission_id=25, task_id=34, name="	Defeat Veger's Precursor robot",
                        rule=lambda state, player:
                        spargus_to_monk_temple(state, player)
                        and state.has("JET-Board", player)
                        and state.has_any("Blaster", "Beam Reflexor", "Vulcan Fury", "Arc Wielder", "Needle Lazer")),
    # Act 2 (Robot Fight Complete)
    26: Jak3MissionData(mission_id=26, task_id=35, name="Reach Port via sewer",
                        rule=lambda state, player:
                        spargus_to_port(state, player)
                        and any_gun(state, player)
                        and state.has("JET-Board", player)),
    27: Jak3MissionData(mission_id=27, task_id=37, name="Destroy incoming blast bots",
                        rule=lambda state, player:
                        spargus_to_port(state, player)
                        and any_gun(state, player)),
    28: Jak3MissionData(mission_id=28, task_id=38, name="Destroy barrier with missile",
                        rule=lambda state, player:
                        spargus_to_port(state, player)),
    29: Jak3MissionData(mission_id=29, task_id=39, name="Beat gun course 1",
                        rule=lambda state, player:
                        spargus_to_port(state, player)
                        and state.has_any("Blaster", "Beam Reflexor", player)),
    30: Jak3MissionData(mission_id=30, task_id=40, name="Destroy sniper cannons",
                        rule=lambda state, player:
                        port_to_inda(state, player)),
    31: Jak3MissionData(mission_id=31, task_id=41, name="Reach Metal Head area via sewer",
                        rule=lambda state, player:
                        port_to_inda(state, player)
                        and any_gun(state, player)
                        and state.has("JET-Board", player)),
    32: Jak3MissionData(mission_id=32, task_id=42, name="Destroy dark eco tanks",
                        rule=lambda state, player:
                        port_to_metal_head_section(state, player)
                        and state.has("JET-Board", player)),
    33: Jak3MissionData(mission_id=33, task_id=43, name="Kill dark plants in forest",
                        rule=lambda state, player:
                        port_to_metal_head_section(state, player)
                        and state.has("JET-Board", player)),
    34: Jak3MissionData(mission_id=34, task_id=44, name="Destroy eco grid with Jinx",
                        rule=lambda state, player:
                        port_to_metal_head_section(state, player)
                        and any_gun(state, player)),
    35: Jak3MissionData(mission_id=35, task_id=45, name="Hijack eco vehicle",
                        rule=lambda state, player:
                        port_to_indb(state, player)),
    36: Jak3MissionData(mission_id=36, task_id=46, name="Defend Port from attack",
                        rule=lambda state, player:
                        spargus_to_port(state, player)
                        and any_gun(state, player)),
    37: Jak3MissionData(mission_id=37, task_id=47, name="Beat gun course 2",
                        rule=lambda state, player:
                        spargus_to_port(state, player)
                        and state.has("Scatter Gun", "Wave Concussor", player)),
    38: Jak3MissionData(mission_id=38, task_id=48, name="Break barrier with blast bot",
                        rule=lambda state, player:
                        port_to_indb(state, player)),
    39: Jak3MissionData(mission_id=39, task_id=49, name="Defend HQ from attack",
                        rule=lambda state, player:
                        port_to_hq(state, player)
                        and any_gun(state, player)),
    40: Jak3MissionData(mission_id=40, task_id=50, name="Find switch in sewers",
                        rule=lambda state, player:
                        port_to_hq(state, player)
                        and any_gun(state, player)
                        and state.has("JET-Board", player)),
    41: Jak3MissionData(mission_id=41, task_id=51, name="Find cypher in eco grid",
                        rule=lambda state, player:
                        port_to_inda(state, player)),
    42: Jak3MissionData(mission_id=42, task_id=52, name="Race for more artifacts",
                        rule=lambda state, player:
                        state.has("Gate Pass to Spargus", "Sand Shark", player)),
    43: Jak3MissionData(mission_id=43, task_id=53, name="Destroy metal-pedes in nest",
                        rule=lambda state, player:
                        spargus_to_nest(state, player)),
    44: Jak3MissionData(mission_id=44, task_id=54, name="Chase down metal head beasts",
                        rule=lambda state, player:
                        spargus_to_nest(state, player)),
    45: Jak3MissionData(mission_id=45, task_id=55, name="Defend Spargus' front gate",
                        rule=lambda state, player:
                        car_with_guns(state, player)),
    46: Jak3MissionData(mission_id=46, task_id=56, name="Take out Marauder stronghold",
                        rule=lambda state, player:
                        spargus_to_nest(state, player)),
    47: Jak3MissionData(mission_id=47, task_id=57, name="Beat pillar ring challenges",
                        rule=lambda state, player:
                        port_to_metal_head_section(state, player)
                        and state.has_all("Holo Cube", "Beam Generator", "Prism", "Quantum Reflector", "JET-Board")),
    48: Jak3MissionData(mission_id=48, task_id=58, name="Destroy war factory defenses",
                        rule=lambda state, player:
                        port_to_hq(state, player)
                        and any_gun(state, player)
                        and state.has("Cypher Glyph")),
    49: Jak3MissionData(mission_id=49, task_id=59, name="Explore war factory",
                        rule=lambda state, player:
                        port_to_hq(state, player)
                        and any_gun(state, player)
                        and state.has("Cypher Glyph")),
    50: Jak3MissionData(mission_id=50, task_id=60, name="Beat Cyber Errol boss",
                        rule=lambda state, player:
                        port_to_hq(state, player)
                        and any_gun(state, player)
                        and state.has("Cypher Glyph")),
    # Act 3 (Tomb Baron Fight Complete)
    51: Jak3MissionData(mission_id=51, task_id=61, name="Rescue Seem at temple",
                        rule=lambda state, player:
                        spargus_to_monk_temple(state, player)
                        and any_gun(state, player)
                        and state.has_all(("Dark Jak", "Dark Strike", "Light Jak", "Light Flight"), player)),
    52: Jak3MissionData(mission_id=52, task_id=62, name="Defend Spargus from attack",
                        rule=lambda state, player:
                        state.has_all("War Amulet #1", "War Amulet #2", "Gun Turret", player)),
    53: Jak3MissionData(mission_id=53, task_id=63, name="Activate Astro-Viewer in Haven Forest",
                        rule=lambda state, player:
                        slums_to_port(state, player)
                        and state.has("JET-Board", player)),
    54: Jak3MissionData(mission_id=54, task_id=64, name="Get Life Seed in Dead Town",
                        rule=lambda state, player:
                        any_gun(state, player)
                        and state.has("Titan Suit", player)),
    55: Jak3MissionData(mission_id=55, task_id=65, name="Protect Samos in Haven Forest",
                        rule=lambda state, player:
                        slums_to_market(state, player)
                        and any_gun(state, player)
                        and state.has("Life Seed", player)),
    56: Jak3MissionData(mission_id=56, task_id=66, name="Destroy Drill Platform Tower",
                        rule=lambda state, player:
                        slums_to_port(state, player)
                        and (state.has("Titan Suit", player)
                             and state.has_any(("Blaster", "Vulcan Fury"), player))),
    57: Jak3MissionData(mission_id=57, task_id=67, name="Rescue Lurkers for Brutter #2",
                        rule=lambda state, player:
                        slums_to_market(state, player)
                        and (state.has("Yellow Security Pass", player))
                        and any_gun(state, player)),
    58: Jak3MissionData(mission_id=58, task_id=68, name="Win Class 1 Race at Stadium",
                        rule=lambda state, player:
                        slums_to_stadium(state, player)),
    59: Jak3MissionData(mission_id=59, task_id=69, name="Explore Palace",
                        rule=lambda state, player:
                        slums_to_market(state, player)
                        and state.has_all(("JET-Board", "Purple Security Pass"), player)
                        and any_gun(state, player)),
    60: Jak3MissionData(mission_id=60, task_id=70, name="Get Heart of Mar in Weapons Lab",
                        rule=lambda state, player:
                        slums_to_landing(state, player)
                        and state.has("Black Security Pass", player)
                        and any_gun(state, player)),
    61: Jak3MissionData(mission_id=60, task_id=71, name="Beat Krew in Weapons Lab",
                        rule=lambda state, player:
                        slums_to_landing(state, player)
                        and state.has("Black Security Pass", player)
                        and any_gun(state, player)),
}


main_tasks_to_missions = {miss.task_id: miss for _, miss in main_mission_table.items()}


# Names of Side Missions are taken from the Fandom Jak II Wiki
# ID numbers are precalculated and offset by 100 to distinguish them from main missions.
side_mission_table = {
    # Orb Searches
    101: Jak3SideMissionData(mission_id=101, task_id=73, name="Orb Search 1 (Computer #2)"),
    102: Jak3SideMissionData(mission_id=102, task_id=74, name="Orb Search 2 (Computer #3)",
                             rule=lambda state, player:
                             slums_to_port(state, player)),
    103: Jak3SideMissionData(mission_id=103, task_id=75, name="Orb Search 3 (Computer #4)",
                             rule=lambda state, player:
                             slums_to_port(state, player)),
    104: Jak3SideMissionData(mission_id=104, task_id=76, name="Orb Search 4 (Computer #5)"),
    105: Jak3SideMissionData(mission_id=105, task_id=77, name="Orb Search 5 (Computer #9)",
                             rule=lambda state, player:
                             slums_to_market(state, player)),
    106: Jak3SideMissionData(mission_id=106, task_id=78, name="Orb Search 6 (Computer #10)",
                             rule=lambda state, player:
                             slums_to_market(state, player)),
    107: Jak3SideMissionData(mission_id=107, task_id=79, name="Orb Search 7 (Computer #11)",
                             rule=lambda state, player:
                             slums_to_market(state, player)),
    108: Jak3SideMissionData(mission_id=108, task_id=80, name="Orb Search 8 (Computer #12)",
                             rule=lambda state, player:
                             slums_to_market(state, player)),
    109: Jak3SideMissionData(mission_id=109, task_id=81, name="Orb Search 9 (Computer #6)",
                             rule=lambda state, player:
                             slums_to_stadium(state, player)),
    110: Jak3SideMissionData(mission_id=110, task_id=82, name="Orb Search 10 (Computer #14)",
                             rule=lambda state, player:
                             slums_to_port(state, player)),
    111: Jak3SideMissionData(mission_id=111, task_id=83, name="Orb Search 11 (Computer #15)",
                             rule=lambda state, player:
                             slums_to_stadium(state, player)),
    112: Jak3SideMissionData(mission_id=112, task_id=84, name="Orb Search 12 (Computer #7)",
                             rule=lambda state, player:
                             slums_to_market(state, player)),
    113: Jak3SideMissionData(mission_id=113, task_id=85, name="Orb Search 13 (Computer #16)",
                             rule=lambda state, player:
                             state.has("Green Security Pass", player)),
    114: Jak3SideMissionData(mission_id=114, task_id=86, name="Orb Search 14 (Computer #17)",
                             rule=lambda state, player:
                             slums_to_stadium(state, player)),
    115: Jak3SideMissionData(mission_id=115, task_id=87, name="Orb Search 15 (Computer #18)",
                             rule=lambda state, player:
                             slums_to_market(state, player)),
    116: Jak3SideMissionData(mission_id=116, task_id=88, name="Orb Search 15 (Computer #18)",
                             rule=lambda state, player:
                             slums_to_market(state, player)),
    117: Jak3SideMissionData(mission_id=117, task_id=89, name="Orb Search 15 (Computer #18)",
                             rule=lambda state, player:
                             slums_to_market(state, player)),
    118: Jak3SideMissionData(mission_id=118, task_id=90, name="Orb Search 15 (Computer #18)",
                             rule=lambda state, player:
                             slums_to_market(state, player)),
    119: Jak3SideMissionData(mission_id=119, task_id=91, name="Orb Search 15 (Computer #18)",
                             rule=lambda state, player:
                             slums_to_market(state, player)),
    120: Jak3SideMissionData(mission_id=120, task_id=92, name="Orb Search 15 (Computer #18)",
                             rule=lambda state, player:
                             slums_to_market(state, player)),
    121: Jak3SideMissionData(mission_id=121, task_id=93, name="Orb Search 15 (Computer #18)",
                             rule=lambda state, player:
                             slums_to_market(state, player)),
    122: Jak3SideMissionData(mission_id=119, task_id=94, name="Orb Search 15 (Computer #18)",
                             rule=lambda state, player:
                             slums_to_market(state, player)),
    123: Jak3SideMissionData(mission_id=119, task_id=95, name="Orb Search 15 (Computer #18)",
                             rule=lambda state, player:
                             slums_to_market(state, player)),
    124: Jak3SideMissionData(mission_id=119, task_id=96, name="Orb Search 15 (Computer #18)",
                             rule=lambda state, player:
                             slums_to_market(state, player)),
    125: Jak3SideMissionData(mission_id=125, task_id=97, name="Orb Search 15 (Computer #18)",
                             rule=lambda state, player:
                             slums_to_market(state, player)),
    126: Jak3SideMissionData(mission_id=126, task_id=98, name="Orb Search 15 (Computer #18)",
                             rule=lambda state, player:
                             slums_to_market(state, player)),
    127: Jak3SideMissionData(mission_id=127, task_id=99, name="Orb Search 15 (Computer #18)",
                             rule=lambda state, player:
                             slums_to_market(state, player)),
    128: Jak3SideMissionData(mission_id=128, task_id=100, name="Orb Search 15 (Computer #18)",
                             rule=lambda state, player:
                             slums_to_market(state, player)),
    129: Jak3SideMissionData(mission_id=129, task_id=101, name="Orb Search 15 (Computer #18)",
                             rule=lambda state, player:
                             slums_to_market(state, player)),
    130: Jak3SideMissionData(mission_id=130, task_id=102, name="Orb Search 15 (Computer #18)",
                             rule=lambda state, player:
                             slums_to_market(state, player)),
    131: Jak3SideMissionData(mission_id=131, task_id=103, name="Orb Search 15 (Computer #18)",
                             rule=lambda state, player:
                             slums_to_market(state, player)),
    132: Jak3SideMissionData(mission_id=132, task_id=104, name="Orb Search 15 (Computer #18)",
                             rule=lambda state, player:
                             slums_to_market(state, player)),
    133: Jak3SideMissionData(mission_id=133, task_id=105, name="Orb Search 15 (Computer #18)",
                             rule=lambda state, player:
                             slums_to_market(state, player)),
    134: Jak3SideMissionData(mission_id=134, task_id=106, name="Orb Search 15 (Computer #18)",
                             rule=lambda state, player:
                             slums_to_market(state, player)),
    135: Jak3SideMissionData(mission_id=135, task_id=107, name="Orb Search 15 (Computer #18)",
                             rule=lambda state, player:
                             slums_to_market(state, player)),
    136: Jak3SideMissionData(mission_id=136, task_id=108, name="Orb Search 15 (Computer #18)",
                             rule=lambda state, player:
                             slums_to_market(state, player)),
    137: Jak3SideMissionData(mission_id=137, task_id=109, name="Orb Search 15 (Computer #18)",
                             rule=lambda state, player:
                             slums_to_market(state, player)),
    138: Jak3SideMissionData(mission_id=138, task_id=110, name="Orb Search 15 (Computer #18)",
                             rule=lambda state, player:
                             slums_to_market(state, player)),
    139: Jak3SideMissionData(mission_id=139, task_id=111, name="Orb Search 15 (Computer #18)",
                             rule=lambda state, player:
                             slums_to_market(state, player)),
    140: Jak3SideMissionData(mission_id=140, task_id=112, name="Orb Search 15 (Computer #18)",
                             rule=lambda state, player:
                             slums_to_market(state, player)),
    141: Jak3SideMissionData(mission_id=141, task_id=113, name="Orb Search 15 (Computer #18)",
                             rule=lambda state, player:
                             slums_to_market(state, player)),
    ## Ring Side Missions
    142: Jak3SideMissionData(mission_id=142, task_id=114, name="Orb Search 15 (Computer #18)",
                             rule=lambda state, player:
                             slums_to_market(state, player)),
    143: Jak3SideMissionData(mission_id=143, task_id=115, name="Orb Search 15 (Computer #18)",
                             rule=lambda state, player:
                             slums_to_market(state, player)),
    144: Jak3SideMissionData(mission_id=144, task_id=116, name="Orb Search 15 (Computer #18)",
                             rule=lambda state, player:
                             slums_to_market(state, player)),
    145: Jak3SideMissionData(mission_id=145, task_id=117, name="Orb Search 15 (Computer #18)",
                             rule=lambda state, player:
                             slums_to_market(state, player)),
    146: Jak3SideMissionData(mission_id=146, task_id=118, name="Orb Search 15 (Computer #18)",
                             rule=lambda state, player:
                             slums_to_market(state, player)),
    147: Jak3SideMissionData(mission_id=147, task_id=119, name="Orb Search 15 (Computer #18)",
                             rule=lambda state, player:
                             slums_to_market(state, player)),
}


side_tasks_to_missions = {miss.task_id: miss for _, miss in side_mission_table.items()}
