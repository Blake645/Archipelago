from .rules import (spargus_to_desert, spargus_to_nest, spargus_to_port, port_to_inda,
                    port_to_indb, port_to_hq, port_to_ruins)
from .locs.mission_locations import main_mission_table, side_mission_table


def _always(state, player) -> bool:
    return True

def _jet(state, player) -> bool:
    return state.has("JET-Board", player)

def _m(mission_id):
    return main_mission_table[mission_id].rule

def _s(mission_id):
    return side_mission_table[mission_id].rule

def _and(*rules):
    return lambda state, player: all(r(state, player) for r in rules)


# (label, orb count, access rule) - an area's orbs count once its rule passes
AREA_ORBS = [
    ("Spargus",                31, _always),
    ("Spargus (JET-Board)",    25, _jet),

    ("Monk Temple - tower",    3,  _m(16)),
    ("Monk Temple - oracle",   1,  _m(19)),
    ("Monk Temple - tests",    2,  _m(21)),
    ("Monk Temple - Seem",     11, _m(51)),

    ("Metal Head Nest",        8,  _m(15)),

    ("Sewers - Port route",    4,  _m(26)),
    ("Sewers - Metal Head",    3,  _m(31)),
    ("Sewers - switch",        6,  _m(40)),

    ("Port",                   30, _m(26)),
    ("Industrial Section A",   8,  _and(port_to_inda, _jet)),
    ("Industrial Section B",   5,  _and(port_to_indb, _jet)),
    ("Slums / New Haven",      14, _and(port_to_hq, _jet)),

    ("Outside Palace Ruins",   8,  port_to_ruins),
    ("Ruined Stadium",         10, _m(57)),
]

# side mission id -> main mission ids that must be completable first
_SIDE_REQ = {
    # Spargus orb searches / races
    115: (3,), 116: (7,), 117: (8,), 118: (9,), 119: (11,), 120: (20,),
    121: (42,), 122: (42,),
    144: (3,), 145: (13,), 150: (20,), 153: (42,),
    # Wasteland (desert) orb searches / races / others
    101: (6,), 102: (9,), 103: (9,), 104: (10,), 105: (10,), 106: (11,), 107: (11,),
    108: (19, 15),
    109: (20,), 110: (34,), 111: (42,), 112: (44,), 113: (46,), 114: (46,),
    149: (9,), 152: (20,), 142: (20,), 143: (44,),
    148: (42,), 157: (20,),
    # Haven City orb searches (id = 122 + wiki number)
    123: (25,), 124: (25,), 125: (26,), 126: (27,), 127: (28,),
    128: (29,), 129: (29, 30), 130: (34,), 131: (34,), 132: (34,),
    133: (35,), 134: (47,), 135: (38,), 136: (38,), 137: (39,),
    138: (41,), 139: (54,), 140: (56,), 141: (56,),
    # Haven City races / others
    147: (34,), 146: (38,), 151: (38,),
    156: (28,), 164: (28,),
}

SIDE_MISSION_ORBS = {}
for _i in range(101, 142):                 # orb searches, 3 orbs each
    SIDE_MISSION_ORBS[_i] = 3
for _i in (142, 143, 144, 145, 146, 147, 149, 150, 151, 152, 153):   # races, 10 each
    SIDE_MISSION_ORBS[_i] = 10
for _i in (148, 156, 157, 164):            # unique missions + JET-Board game, 18 each
    SIDE_MISSION_ORBS[_i] = 18

# Minigame medals: 3 orbs x (bronze, silver, gold) = 9 orbs per minigame
MINIGAME_ORBS = []
_MEDAL_MINIGAMES = [
    ("Daxter Pac-man",                  _m(41)),
    ("Blaster Gun Course",              _m(29)),
    ("Scatter Gun Course",              _m(37)),
    ("Satellite Minigame",              spargus_to_desert),   # the minigame is in the desert
    ("Gun Turret Minigame",             _m(13)),
    ("Air Time Challenge",              _s(158)),
    ("Total Air Time Challenge",        _s(159)),
    ("Jump Distance Challenge",         _s(160)),
    ("Total Jump Distance Challenge",   _s(161)),
    ("Roll Count Challenge",            _s(162)),
    ("Destroy Marauders",               _s(163)),
    ("JET-Board Side Mission (Ind. A)", _s(164)),
    ("Desert Time Trial",               _s(154)),
    ("Desert Rally",                    _s(155)),
]
for _name, _rule in _MEDAL_MINIGAMES:
    MINIGAME_ORBS.append((_name + " medals", 9, _rule))

for _sid, _count in SIDE_MISSION_ORBS.items():
    if _count > 0:
        _rules = [_s(_sid)] + [_m(r) for r in _SIDE_REQ.get(_sid, ())]
        AREA_ORBS.append((side_mission_table[_sid].name, _count, _and(*_rules)))
for _label, _count, _rule in MINIGAME_ORBS:
    if _count > 0:
        AREA_ORBS.append((_label, _count, _rule))

ORB_SLACK = 1.0  # only trust 95% of the counted orbs (set to 1.0 for no margin)


def total_logic_orbs() -> int:
    return int(sum(c for _, c, _ in AREA_ORBS) * ORB_SLACK)

def reachable_orbs(state, player) -> int:
    # Cached on the state; Jak3World.collect/remove reset the "Fresh" flag
    # whenever the player's items change.
    pi = state.prog_items[player]
    if pi["Reachable Orbs Fresh"]:
        return pi["Reachable Orbs"]
    total = int(sum(c for _, c, rule in AREA_ORBS if rule(state, player)) * ORB_SLACK)
    pi["Reachable Orbs"] = total
    pi["Reachable Orbs Fresh"] = 1
    return total

def can_reach_orbs(state, player, needed: int) -> bool:
    return reachable_orbs(state, player) >= needed