from typing import Callable, Optional
from worlds.jak3.rules import (spargus_to_desert, spargus_to_monk_temple, spargus_to_nest, spargus_to_port, port_to_metal_head_section,
port_to_inda, port_to_indb, port_to_hq, port_to_ruins, any_gun, car_with_guns)


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
                        and state.has_any(("Blaster", "Beam Reflexor", "Vulcan Fury", "Arc Wielder", "Needle Lazer"), player)),
    18: Jak3MissionData(mission_id=18, task_id=27, name="Find satellite in volcano",
                        rule=lambda state, player:
                        spargus_to_monk_temple(state, player)
                        and any_gun(state, player)),
    19: Jak3MissionData(mission_id=19, task_id=28, name="Find oracle in Monk Temple",
                        rule=lambda state, player:
                        spargus_to_monk_temple(state, player)
                        and state.has_all(("Wave Concussor", "Dark Invisibility"), player)),
    20: Jak3MissionData(mission_id=20, task_id=29, name="Defend Ashelin at oasis",
                        rule=lambda state, player:
                        spargus_to_desert(state, player)
                        and any_gun(state, player)),
    21: Jak3MissionData(mission_id=21, task_id=30, name="Complete Monk Temple tests",
                        rule=lambda state, player:
                        spargus_to_monk_temple(state, player)
                        and state.has_all(("Seal of Mar", "JET-Board", "Light Jak" "Light Flash Freeze"), player)),
    22: Jak3MissionData(mission_id=22, task_id=31, name="Travel through catacomb subrails",
                        rule=lambda state, player:
                        spargus_to_monk_temple(state, player)
                        and state.has_all(("Seal of Mar", "JET-Board", "Light Jak" "Light Flash Freeze"), player)),
    23: Jak3MissionData(mission_id=23, task_id=32, name="Explore eco mine",
                        rule=lambda state, player:
                        spargus_to_monk_temple(state, player)
                        and state.has("JET-Board", player)
                        and state.has_any(("Blaster", "Beam Reflexor", "Vulcan Fury", "Arc Wielder", "Needle Lazer"), player)),
    24: Jak3MissionData(mission_id=24, task_id=33, name="Escort bomb train",
                        rule=lambda state, player:
                        spargus_to_monk_temple(state, player)
                        and state.has("JET-Board", player)
                        and state.has_any(("Blaster", "Beam Reflexor", "Vulcan Fury", "Arc Wielder", "Needle Lazer"), player)),
    25: Jak3MissionData(mission_id=25, task_id=34, name="Defeat Veger's Precursor robot",
                        rule=lambda state, player:
                        spargus_to_monk_temple(state, player)
                        and state.has("JET-Board", player)
                        and state.has_any(("Blaster", "Beam Reflexor", "Vulcan Fury", "Arc Wielder", "Needle Lazer"), player)),
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
                        and state.has_any(("Blaster", "Beam Reflexor"), player)),
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
                        and state.has(("Scatter Gun", "Wave Concussor"), player)),
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
                        state.has(("Gate Pass to Spargus", "Sand Shark"), player)),
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
                        and state.has_all(("Holo Cube", "Beam Generator", "Prism", "Quantum Reflector", "JET-Board"), player)),
    48: Jak3MissionData(mission_id=48, task_id=58, name="Destroy war factory defenses",
                        rule=lambda state, player:
                        port_to_hq(state, player)
                        and any_gun(state, player)
                        and state.has("Cypher Glyph", player)),
    49: Jak3MissionData(mission_id=49, task_id=59, name="Explore war factory",
                        rule=lambda state, player:
                        port_to_hq(state, player)
                        and any_gun(state, player)
                        and state.has("Cypher Glyph", player)),
    50: Jak3MissionData(mission_id=50, task_id=60, name="Beat Cyber Errol boss",
                        rule=lambda state, player:
                        port_to_hq(state, player)
                        and any_gun(state, player)
                        and state.has("Cypher Glyph", player)),
    # Act 3 (Tomb Baron Fight Complete)
    51: Jak3MissionData(mission_id=51, task_id=61, name="Rescue Seem at temple",
                        rule=lambda state, player:
                        spargus_to_monk_temple(state, player)
                        and any_gun(state, player)
                        and state.has_all(("Dark Jak", "Dark Strike", "Light Jak", "Light Flight"), player)),
    52: Jak3MissionData(mission_id=52, task_id=62, name="Defend Spargus from attack",
                        rule=lambda state, player:
                        state.has_all(("War Amulet #1", "War Amulet #2", "Gun Turret"), player)),
    53: Jak3MissionData(mission_id=53, task_id=63, name="Activate Astro-Viewer in Haven Forest",
                        rule=lambda state, player:
                        port_to_metal_head_section(state, player)
                        and any_gun(state, player)
                        and state.has_all(("Time Map", "Holo Cube", "Beam Generator", "Prism", "Quantum Reflector"), player)),
    54: Jak3MissionData(mission_id=54, task_id=64, name="	Destroy dark ship shield",
                        rule=lambda state, player:
                        port_to_metal_head_section(state, player)
                        and any_gun(state, player)
                        and state.has_all(("Time Map", "Holo Cube", "Beam Generator", "Prism", "Quantum Reflector"), player)),
    55: Jak3MissionData(mission_id=55, task_id=65, name="Blow open tower door",
                        rule=lambda state, player:
                        port_to_hq(state, player)
                        and state.has("Pass to Metal Head Section", player)),
    56: Jak3MissionData(mission_id=56, task_id=66, name="Destroy Metal Head tower",
                        rule=lambda state, player:
                        port_to_metal_head_section(state, player)
                        and any_gun(state, player)
                        and state.has_all(("Light Jak", "Light Flight"), player)),
    57: Jak3MissionData(mission_id=57, task_id=67, name="Reach catacombs via palace ruins",
                        rule=lambda state, player:
                        port_to_ruins(state, player)
                        and any_gun(state, player)
                        and state.has_all(("War Amulet #1", "War Amulet #2", "War Amulet #3", "JET-Board", "Light Jak", "Light Flight", "Dark Jak", "Dark Strike"), player)),
    58: Jak3MissionData(mission_id=58, task_id=68, name="Break through ruins",
                        rule=lambda state, player:
                        port_to_ruins(state, player)
                        and any_gun(state, player)
                        and state.has_all(("Slam Dozer", "Sand Shark", "Dark Eco Crystal", "Dark Eco Crystal", "Dark Eco Crystal", "Dark Eco Crystal", "Light Eco Crystal", "Light Eco Crystal", "Light Eco Crystal", "Light Eco Crystal",
                                          "War Amulet #1", "War Amulet #2", "War Amulet #3", "JET-Board", "Light Jak", "Light Flight", "Dark Jak", "Dark Strike"),player)),
    59: Jak3MissionData(mission_id=59, task_id=69, name="Reach Precursor core",
                        rule=lambda state, player:
                        port_to_ruins(state, player)
                        and any_gun(state, player)
                        and state.has_all(("Slam Dozer", "Sand Shark", "Dark Eco Crystal", "Dark Eco Crystal", "Dark Eco Crystal", "Dark Eco Crystal", "Light Eco Crystal", "Light Eco Crystal", "Light Eco Crystal", "Light Eco Crystal",
                                          "War Amulet #1", "War Amulet #2", "War Amulet #3", "JET-Board", "Light Jak", "Light Flight", "Dark Jak", "Dark Strike"),player)),
    60: Jak3MissionData(mission_id=60, task_id=70, name="Destroy dark ship",
                        rule=lambda state, player:
                        port_to_ruins(state, player)
                        and any_gun(state, player)
                        and state.has_all(("Slam Dozer", "Sand Shark", "Dark Eco Crystal", "Dark Eco Crystal", "Dark Eco Crystal", "Dark Eco Crystal", "Light Eco Crystal", "Light Eco Crystal", "Light Eco Crystal", "Light Eco Crystal",
                                          "Amulet #1", "Amulet #2", "Amulet #3", "JET-Board", "Light Jak", "Light Flight", "Dark Jak", "Dark Strike"), player)),
    61: Jak3MissionData(mission_id=61, task_id=71, name="Destroy final boss",
                        rule=lambda state, player:
                        port_to_ruins(state, player)
                        and any_gun(state, player)
                        and state.has_all(("Slam Dozer", "Sand Shark", "Dark Eco Crystal", "Dark Eco Crystal", "Dark Eco Crystal", "Dark Eco Crystal", "Light Eco Crystal", "Light Eco Crystal", "Light Eco Crystal", "Light Eco Crystal",
                                          "Amulet #1", "Amulet #2", "Amulet #3", "JET-Board", "Light Jak", "Light Flight", "Dark Jak", "Dark Strike"), player)),
}


main_tasks_to_missions = {miss.task_id: miss for _, miss in main_mission_table.items()}


# Names of Side Missions are taken from the Fandom Jak 3 Wiki
# ID numbers are precalculated and offset by 100 to distinguish them from main missions.
side_mission_table = {
    # Orb Searches
    101: Jak3SideMissionData(mission_id=101, task_id=73, name=" Desert Orb Search 1",
                             rule=lambda state, player:
                             spargus_to_desert(state, player)),
    102: Jak3SideMissionData(mission_id=102, task_id=74, name="Desert Orb Search 2",
                             rule=lambda state, player:
                             spargus_to_desert(state, player)),
    103: Jak3SideMissionData(mission_id=103, task_id=75, name=" Desert Orb Search 3",
                             rule=lambda state, player:
                             spargus_to_desert(state, player)),
    104: Jak3SideMissionData(mission_id=104, task_id=76, name="Desert Orb Search 4",
                             rule=lambda state, player:
                             spargus_to_desert(state, player)),
    105: Jak3SideMissionData(mission_id=105, task_id=77, name="Desert Orb Search 5",
                             rule=lambda state, player:
                             spargus_to_desert(state, player)),
    106: Jak3SideMissionData(mission_id=106, task_id=78, name="Desert Orb Search 6",
                             rule=lambda state, player:
                             spargus_to_desert(state, player)),
    107: Jak3SideMissionData(mission_id=107, task_id=79, name="Desert Orb Search 7",
                             rule=lambda state, player:
                             spargus_to_desert(state, player)),
    108: Jak3SideMissionData(mission_id=108, task_id=80, name="Desert Orb Search 8",
                             rule=lambda state, player:
                             spargus_to_desert(state, player)),
    109: Jak3SideMissionData(mission_id=109, task_id=81, name="Desert Orb Search 9",
                             rule=lambda state, player:
                             spargus_to_desert(state, player)),
    110: Jak3SideMissionData(mission_id=110, task_id=82, name="Desert Orb Search 10",
                             rule=lambda state, player:
                             spargus_to_desert(state, player)),
    111: Jak3SideMissionData(mission_id=111, task_id=83, name="Desert Orb Search 11",
                             rule=lambda state, player:
                             spargus_to_desert(state, player)
                             and state.has("JET-Board", player)),
    112: Jak3SideMissionData(mission_id=112, task_id=84, name="Desert Orb Search 12",
                             rule=lambda state, player:
                             spargus_to_desert(state, player)
                             and state.has("JET-Board", player)),
    113: Jak3SideMissionData(mission_id=113, task_id=85, name="Desert Orb Search 13",
                             rule=lambda state, player:
                             spargus_to_desert(state, player)
                             and state.has("JET-Board", player)),
    114: Jak3SideMissionData(mission_id=114, task_id=86, name="Desert Orb Search 14",
                             rule=lambda state, player:
                             spargus_to_desert(state, player)
                             and state.has("JET-Board", player)),
    115: Jak3SideMissionData(mission_id=115, task_id=87, name="Spargus Orb Search 1"),
    116: Jak3SideMissionData(mission_id=116, task_id=88, name="Desert Orb Search 15",
                             rule=lambda state, player:
                             spargus_to_desert(state, player)
                             and state.has("JET-Board", player)),
    117: Jak3SideMissionData(mission_id=117, task_id=89, name="Spargus Orb Search 2"),
    118: Jak3SideMissionData(mission_id=118, task_id=90, name="Spargus Orb Search 3"),
    119: Jak3SideMissionData(mission_id=119, task_id=91, name="Spargus Orb Search 4"),
    120: Jak3SideMissionData(mission_id=120, task_id=92, name="Spargus Orb Search 5"),
    121: Jak3SideMissionData(mission_id=121, task_id=93, name="Spargus Orb Search 6"),
    122: Jak3SideMissionData(mission_id=122, task_id=94, name="Spargus Orb Search 7"),
    123: Jak3SideMissionData(mission_id=123, task_id=95, name="City Orb Search 1 (Outside Palace Ruins Section)",
                             rule=lambda state, player:
                             port_to_ruins(state, player)),
    124: Jak3SideMissionData(mission_id=124, task_id=96, name="City Orb Search 2 (Outside Palace Ruins Section)",
                             rule=lambda state, player:
                             port_to_ruins(state, player)
                             and state.has("JET-Board", player)),
    125: Jak3SideMissionData(mission_id=125, task_id=97, name="City Orb Search 3 (Outside Palace Ruins Section)",
                             rule=lambda state, player:
                             port_to_ruins(state, player)),
    126: Jak3SideMissionData(mission_id=126, task_id=98, name="City Orb Search 4 (Outside Palace Ruins Section)",
                             rule=lambda state, player:
                             port_to_ruins(state, player)
                             and state.has("JET-Board", player)),
    127: Jak3SideMissionData(mission_id=127, task_id=99, name="City Orb Search 5 (Outside Palace Ruins Section)",
                             rule=lambda state, player:
                             port_to_ruins(state, player)
                             and state.has("JET-Board", player)),
    128: Jak3SideMissionData(mission_id=128, task_id=100, name="City Orb Search 6 (Slums/New Haven Section)",
                             rule=lambda state, player:
                             port_to_hq(state, player)),
    129: Jak3SideMissionData(mission_id=129, task_id=101, name="City Orb Search 7 (Slums/New Haven Section)",
                             rule=lambda state, player:
                             port_to_hq(state, player)),
    130: Jak3SideMissionData(mission_id=130, task_id=102, name="City Orb Search 8 (Slums/New Haven Section)",
                             rule=lambda state, player:
                             port_to_hq(state, player)
                             and state.has("JET-Board", player)),
    131: Jak3SideMissionData(mission_id=131, task_id=103, name="City Orb Search 9 (Slums/New Haven Section)",
                             rule=lambda state, player:
                             port_to_hq(state, player)),
    132: Jak3SideMissionData(mission_id=132, task_id=104, name="City Orb Search 10 (Slums/New Haven Section)",
                             rule=lambda state, player:
                             port_to_hq(state, player)),
    133: Jak3SideMissionData(mission_id=133, task_id=105, name="City Orb Search 11 (Industrial Section B)",
                             rule=lambda state, player:
                             port_to_indb(state, player)),
    134: Jak3SideMissionData(mission_id=134, task_id=106, name="City Orb Search 12 (Industrial Section B)",
                             rule=lambda state, player:
                             port_to_indb(state, player)
                             and state.has("JET-Board", player)),
    135: Jak3SideMissionData(mission_id=135, task_id=107, name="City Orb Search 13 (Industrial Section A)",
                             rule=lambda state, player:
                             port_to_inda(state, player)
                             and state.has("JET-Board", player)),
    136: Jak3SideMissionData(mission_id=136, task_id=108, name="City Orb Search 14 (Industrial Section A)",
                             rule=lambda state, player:
                             port_to_inda(state, player)
                             and state.has("JET-Board", player)),
    137: Jak3SideMissionData(mission_id=137, task_id=109, name="City Orb Search 15 (Industrial Section A)",
                             rule=lambda state, player:
                             port_to_inda(state, player)),
    138: Jak3SideMissionData(mission_id=138, task_id=110, name="City Orb Search 16 (Port)",
                             rule=lambda state, player:
                             spargus_to_port(state, player)),
    139: Jak3SideMissionData(mission_id=139, task_id=111, name="City Orb Search 17 (Port)",
                             rule=lambda state, player:
                             spargus_to_port(state, player)
                             and state.has("JET-Board", player)),
    140: Jak3SideMissionData(mission_id=140, task_id=112, name="City Orb Search 18 (Port)",
                             rule=lambda state, player:
                             spargus_to_port(state, player)
                             and state.has("JET-Board", player)),
    141: Jak3SideMissionData(mission_id=141, task_id=113, name="City Orb Search 19 (Port)",
                             rule=lambda state, player:
                             spargus_to_port(state, player)
                             and state.has("JET-Board", player)),
    ## Ring Side Missions
    142: Jak3SideMissionData(mission_id=142, task_id=114, name="Ring Race #1 (Desert)",
                             rule=lambda state, player:
                             spargus_to_desert(state, player)),
    143: Jak3SideMissionData(mission_id=143, task_id=115, name="Ring Race #2 (Desert)",
                             rule=lambda state, player:
                             spargus_to_desert(state, player)),
    144: Jak3SideMissionData(mission_id=144, task_id=116, name="Ring Race #3 (Spargus)"),
    145: Jak3SideMissionData(mission_id=145, task_id=117, name="Ring Race #4 (Spargus)"),
    146: Jak3SideMissionData(mission_id=146, task_id=118, name="Ring Race #5 (Slums/New Haven Section)",
                             rule=lambda state, player:
                             port_to_hq(state, player)),
    147: Jak3SideMissionData(mission_id=147, task_id=119, name="Ring Race #6 (Industrial Section A)",
                             rule=lambda state, player:
                             port_to_inda(state, player)
                             and state.has("JET-Board", player)),
    ## Other Side Missions
    148: Jak3SideMissionData(mission_id=148, task_id=120, name="Destroy Egg Spiders (Desert)",
                             rule=lambda state, player:
                             spargus_to_desert(state, player)
                             and any_gun(state, player)),
    149: Jak3SideMissionData(mission_id=149, task_id=121, name="Spirit Chase #1 (Desert)",
                             rule=lambda state, player:
                             spargus_to_desert(state, player)),
    150: Jak3SideMissionData(mission_id=150, task_id=122, name="Spirit Chase #2 (Spargus)"),
    151: Jak3SideMissionData(mission_id=151, task_id=123, name="Spirit Chase #1 (Slums/New Haven Section)",
                             rule=lambda state, player:
                             port_to_hq(state, player)),
    152: Jak3SideMissionData(mission_id=152, task_id=124, name="Chase Timer Challenge #1 (Desert)",
                             rule=lambda state, player:
                             spargus_to_desert(state, player)),
    153: Jak3SideMissionData(mission_id=153, task_id=125, name="Chase Timer Challenge #2 (Spargus)"),
    154: Jak3SideMissionData(mission_id=154, task_id=126, name= "Desert Air Time Challenge",
                             rule=lambda state, player:
                             state.has("Gate Pass to Spargus", player)
                             and state.has_any(("Sand Shark", "Heat Seeker", "Dust Demon", "Desert Screamer"), player)),
    155: Jak3SideMissionData(mission_id=155, task_id=127, name="Desert Total Air Time Challenge",
                             rule=lambda state, player:
                             state.has("Gate Pass to Spargus", player)
                             and state.has_any(("Sand Shark", "Heat Seeker", "Dust Demon", "Desert Screamer"), player)),
    156: Jak3SideMissionData(mission_id=156, task_id=128, name="Desert Jump Distance Challenge",
                             rule=lambda state, player:
                             state.has("Gate Pass to Spargus", player)
                             and state.has_any(("Sand Shark", "Heat Seeker", "Dust Demon", "Desert Screamer"), player)),
    157: Jak3SideMissionData(mission_id=157, task_id=129, name="Desert Total Jump Distance Challenge",
                             rule=lambda state, player:
                             state.has("Gate Pass to Spargus", player)
                             and state.has_any(("Sand Shark", "Heat Seeker", "Dust Demon", "Desert Screamer"), player)),
    158: Jak3SideMissionData(mission_id=158, task_id=130, name="Desert Roll Count Challenge",
                             rule=lambda state, player:
                             state.has("Gate Pass to Spargus", player)
                             and state.has_any(("Sand Shark", "Heat Seeker", "Dust Demon", "Desert Screamer"), player)),
    159: Jak3SideMissionData(mission_id=159, task_id=131, name="Desert Time Trial",
                             rule=lambda state, player:
                             spargus_to_desert(state, player)),
    160: Jak3SideMissionData(mission_id=160, task_id=132, name="Desert Rally Side Mission",
                             rule=lambda state, player:
                             spargus_to_desert(state, player)),
    161: Jak3SideMissionData(mission_id=161, task_id=133, name="City Port Attack Side Mission",
                             rule=lambda state, player:
                             spargus_to_port(state, player)),
    162: Jak3SideMissionData(mission_id=162, task_id=134, name="Desert Rescue Side Mission",
                             rule=lambda state, player:
                             state.has_all(("Gate Pass to Spargus", "Sand Shark"), player)),
    163: Jak3SideMissionData(mission_id=163,task_id=135, name="City JET-Board Side Mission",
                             rule=lambda state, player:
                             port_to_inda(state, player)
                             and state.has("JET-Board", player)),
    164: Jak3SideMissionData(mission_id=164, task_id=136, name="Desert Destroy Interceptors Side Mission",
                             rule=lambda state, player:
                             car_with_guns(state, player)),
}


side_tasks_to_missions = {miss.task_id: miss for _, miss in side_mission_table.items()}
MAX_CHECKS_PER_MISSION = 10

def get_location_id(mission_id: int, check_num: int) -> int:
    """Calculate a unique location ID for a mission check.
    Format: mission_id * 100 + check_num (supports up to 99 checks per mission)
    """
    return mission_id * 100 + check_num

def get_all_mission_locations(checks_per_mission: int) -> dict[str, int]:
    """Generate location name -> ID mapping for all missions with given checks per mission."""
    locations = {}
    for mission_id, mission in main_mission_table.items():
        for check in range(1, checks_per_mission + 1):
            name = f"{mission.name} - Check {check}"
            locations[name] = get_location_id(mission_id, check)
    for mission_id, mission in side_mission_table.items():
        for check in range(1, checks_per_mission + 1):
            name = f"{mission.name} - Check {check}"
            locations[name] = get_location_id(mission_id, check)
    return locations

def get_max_mission_locations() -> dict[str, int]:
    """Generate the maximum possible location set (for class-level registration)."""
    return get_all_mission_locations(MAX_CHECKS_PER_MISSION)