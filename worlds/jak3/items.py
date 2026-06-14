from BaseClasses import Item
from .game_id import jak3_name, jak3_max

class Jak3Item(Item):
    game: str = jak3_name


class Jak3ItemData:
    id: int
    name: str
    symbol: str
    
    def __init__(self, item_id: int, name: str, symbol: str) -> None:
        self.item_id = item_id
        self.name = name
        self.symbol = symbol


# ID Range Constants for Item Classification
# These constants define the boundaries for different item types
ITEM_ID_KEY_START = 1           # Key/progression items start at ID 1
ITEM_ID_KEY_END = 33            # Key/progression items end at ID 33
ITEM_ID_FILLER_START = 34       # Filler items start at ID 34 (Dark Eco Pill)
ITEM_ID_FILLER_END = 39         # Standard filler items end at ID 39
TRAP_ID_START = 40               # Trap items start at ID 1 (Trip Trap)
TRAP_ID_END = 56                # Trap items end at ID 17

# Unified Item Table - Single source of truth for all items
# Every item is organized by classification using ID ranges defined above
item_table = {
    # ========== KEY/PROGRESSION ITEMS (IDs 1-33) ==========
    
    # Morph Gun Weapons and Upgrades (IDs 1-12)
    1: Jak3ItemData(item_id=1, name="Scatter Gun", symbol="gun-red-1"),
    2: Jak3ItemData(item_id=2, name="Wave Concussor", symbol="gun-red-2"),
    3: Jak3ItemData(item_id=3, name="Plasmite RPG", symbol="gun-red-3"),
    4: Jak3ItemData(item_id=4, name="Blaster", symbol="gun-yellow-1"),
    5: Jak3ItemData(item_id=5, name="Beam Reflexor", symbol="gun-yellow-2"),
    6: Jak3ItemData(item_id=6, name="Gyro Buster", symbol= "gun-yellow-3"),
    7: Jak3ItemData(item_id=7, name="Vulcan Fury", symbol="gun-blue-1"),
    8: Jak3ItemData(item_id=8, name="Arc Wielder", symbol="gun-blue-2"),
    9: Jak3ItemData(item_id=9, name="Needle Lazer", symbol="gun-blue-3"),
    10: Jak3ItemData(item_id=10, name="Peacemaker", symbol="gun-dark-1"),
    11: Jak3ItemData(item_id=11, name="Mass Inverter", symbol="gun-dark-2"),
    12: Jak3ItemData(item_id=12, name="Super Nova", symbol="gun-dark-3"),

    # Movement Items (IDs 13)
    13: Jak3ItemData(item_id=13, name="JET-Board", symbol="board"),
    
    # Dark Jak Powers (IDs 14-18)
    14: Jak3ItemData(item_id=14, name="Dark Jak", symbol="darkjak"),
    15: Jak3ItemData(item_id=15, name="Dark Bomb", symbol="darkjak-bomb0"),
    16: Jak3ItemData(item_id=16, name="Dark Blast", symbol="darkjak-bomb1"),
    17: Jak3ItemData(item_id=17, name="Dark Invisibility", symbol="artifact-invs"),
    18: Jak3ItemData(item_id=18, name="Dark Strike", symbol="darkjak-smack"),
    
    # Security Passes (IDs 19-25)
    19: Jak3ItemData(item_id=19, name="Gate Pass to Spargus", symbol="pass-front-gate"),
    20: Jak3ItemData(item_id=20, name="Pass to Metal Head Section", symbol="pass-port-mh"),
    21: Jak3ItemData(item_id=21, name="Pass to Industrial Section A", symbol="pass-port-inda"),
    22: Jak3ItemData(item_id=22, name="Pass to Industrial Section B", symbol="pass-inda-indb"),
    23: Jak3ItemData(item_id=23, name="Pass to Slums/New Haven", symbol="pass-indb-sluma"),
    24: Jak3ItemData(item_id=24, name="Pass to Outside Palace Ruins", symbol="pass-slumb-genb"),
    25: Jak3ItemData(item_id=25, name="Air Train Pass", symbol="pass-air-train"),
    
    # Light Jak Powers (IDs 26-30)
    26: Jak3ItemData(item_id=26, name="Light Jak", symbol="lightjak"),
    27: Jak3ItemData(item_id=27, name="Light Regeneration", symbol="lightjak-regen"),
    28: Jak3ItemData(item_id=28, name="Light Flash Freeze", symbol="lightjak-freeze"),
    29: Jak3ItemData(item_id=29, name="Light Shield", symbol="lightjak-shield"),
    30: Jak3ItemData(item_id=30, name="Light Flight", symbol="lightjak-swoop"),

    # Vehicles (IDs 31-38)
    31: Jak3ItemData(item_id=31, name="Tough Puppy", symbol="vehicle-turtle"),
    32: Jak3ItemData(item_id=32, name="Sand Shark", symbol="vehicle-snake"),
    33: Jak3ItemData(item_id=33, name="Gila Stomper", symbol="vehicle-scorpion"),
    34: Jak3ItemData(item_id=34, name="Dune Hopper", symbol="vehicle-toad"),
    35: Jak3ItemData(item_id=35, name="Slam Dozer", symbol="vehicle-rhino"),
    36: Jak3ItemData(item_id=36, name="Heat Seeker", symbol="vehicle-fox"),
    37: Jak3ItemData(item_id=37, name="Dust Demon", symbol="vehicle-mirage"),
    38: Jak3ItemData(item_id=38, name="Desert Screamer", symbol="vehicle-x-ride"),

    # Armor (IDs 39-42)
    39: Jak3ItemData(item_id=39, name="Bracers Armor", symbol="armor0"),
    40: Jak3ItemData(item_id=40, name="Leg Armor", symbol="armor1"),
    41: Jak3ItemData(item_id=41, name="Shoulder Armor", symbol="armor2"),
    42: Jak3ItemData(item_id=42, name="Chest Armor", symbol="armor3"),

    # Miscellaneous Important Items (IDs 43-53)
    43: Jak3ItemData(item_id=43, name="Beam Generator", symbol="av-generator"),
    44: Jak3ItemData(item_id=44, name="Holo Cube", symbol="av-cube"),
    45: Jak3ItemData(item_id=45, name="Time Map", symbol="av-map"),
    46: Jak3ItemData(item_id=46, name="Prism", symbol="av-prism"),
    47: Jak3ItemData(item_id=47, name="Quantum Reflector", symbol="av-reflector"),
    48: Jak3ItemData(item_id=48, name="War Amulet #1", symbol="amulet-1"),
    49: Jak3ItemData(item_id=49, name="War Amulet #2", symbol="amulet-2"),
    50: Jak3ItemData(item_id=50, name="War Amulet #3", symbol="amulet-3"),
    51: Jak3ItemData(item_id=51, name="Cypher Glyph", symbol="cypher-gliph"),
    52: Jak3ItemData(item_id=52, name="Dark Eco Crystal", symbol="dark-eco-crystal"),
    53: Jak3ItemData(item_id=53, name="Light Eco Crystal", symbol="light-eco-crystal"),
    
    # ========== FILLER ITEMS ==========
    # Standard Filler Items (IDs 54-60)
    54: Jak3ItemData(item_id=54, name="Dark Eco Pill", symbol="dark-eco-pill"),
    55: Jak3ItemData(item_id=55, name="Light Eco Pill", symbol="light-eco-pill"),
    56: Jak3ItemData(item_id=56, name="Health Pack", symbol="health-pack"),
    57: Jak3ItemData(item_id=57, name="Scatter Gun Ammo", symbol="ammo-red"),
    58: Jak3ItemData(item_id=58, name="Blaster Ammo", symbol="ammo-yellow"),
    59: Jak3ItemData(item_id=59, name="Vulcan Fury Ammo", symbol="ammo-blue"),
    60: Jak3ItemData(item_id=60, name="Peacemaker Ammo", symbol="ammo-dark"),

    # Trap Items (IDs 40-56)
    # Jak 1 Traps, Reimagined for Jak 2 and 3 (IDs 61-71)
    61: Jak3ItemData(item_id=61, name="Trip Trap", symbol="trip"),
    62: Jak3ItemData(item_id=62, name="Slip Trap", symbol="ice-physics"),
    63: Jak3ItemData(item_id=63, name="Gravity Trap", symbol="the-big-apple"),
    64: Jak3ItemData(item_id=64, name="Camera Trap", symbol="caught-in-4k"),
    65: Jak3ItemData(item_id=65, name="Darkness Trap", symbol="daredevil"),
    66: Jak3ItemData(item_id=66, name="Earthquake Trap", symbol="caseoh"),
    67: Jak3ItemData(item_id=67, name="Teleport Trap", symbol="instant-transmission"),
    68: Jak3ItemData(item_id=68, name="Pacifism Trap", symbol="personal-bubble"),
    69: Jak3ItemData(item_id=69, name="Health Trap", symbol="hit-by-bus"),
    70: Jak3ItemData(item_id=70, name="Ledge Trap", symbol="rivals-of-aether"),
    71: Jak3ItemData(item_id=71, name="Mirror Trap", symbol="man-in-the-mirror"),

    # Jak 2 Traps! (IDs 72-77)
    72: Jak3ItemData(item_id=72, name="High Alert Trap", symbol="five-star"),
    73: Jak3ItemData(item_id=73, name="Ammo Trap", symbol="russian-roulette"),
    74: Jak3ItemData(item_id=74, name="Dark Trap", symbol="anger-issues"),
    75: Jak3ItemData(item_id=75, name="Speed Trap", symbol="sonic-speed"),
    76: Jak3ItemData(item_id=76, name="Slow Trap", symbol="la-traffic"),
    77: Jak3ItemData(item_id=77, name="Hero Trap", symbol="hardcore")
}