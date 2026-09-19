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
ITEM_ID_KEY_START = 1
ITEM_ID_KEY_END = 55
ITEM_ID_FILLER_START = 56  # Filler items start at 56
ITEM_ID_FILLER_END = 63  # Standard filler items end at 63
TRAP_ID_START = 64  # Trap items start at 64
TRAP_ID_END = 80  # Trap items end at 80
SECRET_ID_START = 81  # Archipelago secret unlocks start at 81
SECRET_ID_END = 113  # Archipelago secret unlocks end at 113

item_table = {
    # ========== KEY/PROGRESSION ITEMS (IDs 1-55) ==========

    # Morph Gun Weapons and Upgrades (IDs 1-12)
    1: Jak3ItemData(item_id=1, name="Scatter Gun", symbol="gun-red-1"),
    2: Jak3ItemData(item_id=2, name="Wave Concussor", symbol="gun-red-2"),
    3: Jak3ItemData(item_id=3, name="Plasmite RPG", symbol="gun-red-3"),
    4: Jak3ItemData(item_id=4, name="Blaster", symbol="gun-yellow-1"),
    5: Jak3ItemData(item_id=5, name="Beam Reflexor", symbol="gun-yellow-2"),
    6: Jak3ItemData(item_id=6, name="Gyro Burster", symbol="gun-yellow-3"),
    7: Jak3ItemData(item_id=7, name="Vulcan Fury", symbol="gun-blue-1"),
    8: Jak3ItemData(item_id=8, name="Arc Wielder", symbol="gun-blue-2"),
    9: Jak3ItemData(item_id=9, name="Needle Lazer", symbol="gun-blue-3"),
    10: Jak3ItemData(item_id=10, name="Peacemaker", symbol="gun-dark-1"),
    11: Jak3ItemData(item_id=11, name="Mass Inverter", symbol="gun-dark-2"),
    12: Jak3ItemData(item_id=12, name="Super Nova", symbol="gun-dark-3"),

    # Movement Items (ID 13)
    13: Jak3ItemData(item_id=13, name="JET-Board", symbol="board"),

    # Dark Jak Powers (IDs 14-18)
    14: Jak3ItemData(item_id=14, name="Dark Jak", symbol="darkjak"),
    15: Jak3ItemData(item_id=15, name="Dark Bomb", symbol="darkjak-bomb0"),
    16: Jak3ItemData(item_id=16, name="Dark Blast", symbol="darkjak-bomb1"),
    17: Jak3ItemData(item_id=17, name="Dark Invisibility", symbol="artifact-invis"),
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

    # Miscellaneous Important Items (IDs 43-55)
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
    54: Jak3ItemData(item_id=54, name="Seal of Mar", symbol="seal-of-mar"),
    55: Jak3ItemData(item_id=55, name="Gun Turret", symbol="gun-turret"),

    # ========== FILLER ITEMS (IDs 56-63) ==========
    56: Jak3ItemData(item_id=56, name="Dark Eco Pill", symbol="dark-eco-pill"),
    57: Jak3ItemData(item_id=57, name="Light Eco Pill", symbol="light-eco-pill"),
    58: Jak3ItemData(item_id=58, name="Health Pack", symbol="health-pack"),
    59: Jak3ItemData(item_id=59, name="Scatter Gun Ammo", symbol="ammo-red"),
    60: Jak3ItemData(item_id=60, name="Blaster Ammo", symbol="ammo-yellow"),
    61: Jak3ItemData(item_id=61, name="Vulcan Fury Ammo", symbol="ammo-blue"),
    62: Jak3ItemData(item_id=62, name="Peacemaker Ammo", symbol="ammo-dark"),
    63: Jak3ItemData(item_id=63, name="Skull Gems", symbol="gem"),

    # ========== TRAP ITEMS (IDs 64-80) ==========
    # Jak 1 Traps, Reimagined for Jak 2 and 3 (IDs 64-74)
    64: Jak3ItemData(item_id=64, name="Trip Trap", symbol="trip"),
    65: Jak3ItemData(item_id=65, name="Slip Trap", symbol="ice-physics"),
    66: Jak3ItemData(item_id=66, name="Gravity Trap", symbol="the-big-apple"),
    67: Jak3ItemData(item_id=67, name="Camera Trap", symbol="caught-in-4k"),
    68: Jak3ItemData(item_id=68, name="Darkness Trap", symbol="daredevil"),
    69: Jak3ItemData(item_id=69, name="Earthquake Trap", symbol="caseoh"),
    70: Jak3ItemData(item_id=70, name="Teleport Trap", symbol="instant-transmission"),
    71: Jak3ItemData(item_id=71, name="Pacifism Trap", symbol="personal-bubble"),
    72: Jak3ItemData(item_id=72, name="Health Trap", symbol="hit-by-bus"),
    73: Jak3ItemData(item_id=73, name="Ledge Trap", symbol="rivals-of-aether"),
    74: Jak3ItemData(item_id=74, name="Mirror Trap", symbol="man-in-the-mirror"),

    # Jak 2 Traps (IDs 75-80)
    75: Jak3ItemData(item_id=75, name="Ammo Trap", symbol="russian-roulette"),
    76: Jak3ItemData(item_id=76, name="Dark Trap", symbol="anger-issues"),
    77: Jak3ItemData(item_id=77, name="No Light Trap", symbol="no-light-eco"),
    78: Jak3ItemData (item_id=78,name= "Reverse Trap", symbol="turn-right-to-go-left"),
    79: Jak3ItemData(item_id=79, name="Hero Trap", symbol="hardcore"),
    80: Jak3ItemData(item_id=80, name="Despair Trap", symbol="emotional-damage"),

    # ========== ARCHIPELAGO SECRETS (IDs 81-113) ==========
    81: Jak3ItemData(item_id=81, name="Secret - Increased Red Ammo Capacity", symbol="secret-gun-ammo-red"),
    82: Jak3ItemData(item_id=82, name="Secret - Increased Yellow Ammo Capacity", symbol="secret-gun-ammo-yellow"),
    83: Jak3ItemData(item_id=83, name="Secret - Increased Blue Ammo Capacity", symbol="secret-gun-ammo-blue"),
    84: Jak3ItemData(item_id=84, name="Secret - Increased Dark Ammo Capacity", symbol="secret-gun-ammo-dark"),
    85: Jak3ItemData(item_id=85, name="Secret - Blaster Damage Upgrade", symbol="secret-gun-yellow-1"),
    86: Jak3ItemData(item_id=86, name="Secret - Scatter Gun Rate-of-Fire Upgrade", symbol="secret-gun-red-1"),
    87: Jak3ItemData(item_id=87, name="Secret - Vulcan Fury Damage Upgrade", symbol="secret-gun-blue-1"),
    88: Jak3ItemData(item_id=88, name="Secret - Peace Maker Increased Radius", symbol="secret-gun-dark-1"),
    89: Jak3ItemData(item_id=89, name="Secret - Reflexor Increased Deflections", symbol="secret-gun-yellow-2"),
    90: Jak3ItemData(item_id=90, name="Secret - Concussor Damage Upgrade", symbol="secret-gun-red-2"),
    91: Jak3ItemData(item_id=91, name="Secret - Arc Wielder Robot Shock", symbol="secret-gun-blue-2"),
    92: Jak3ItemData(item_id=92, name="Secret - Mass Inverter Duration Upgrade", symbol="secret-gun-dark-2"),
    93: Jak3ItemData(item_id=93, name="Secret - Gyro Burster Duration Upgrade", symbol="secret-gun-yellow-3"),
    94: Jak3ItemData(item_id=94, name="Secret - Plasmite RPG Ammo Efficiency", symbol="secret-gun-red-3"),
    95: Jak3ItemData(item_id=95, name="Secret - Needle Lazer Ammo Efficiency", symbol="secret-gun-blue-3"),
    96: Jak3ItemData(item_id=96, name="Secret - Super Nova Ammo Efficiency", symbol="secret-gun-dark-3"),
    97: Jak3ItemData(item_id=97, name="Secret - Upgrade Vehicle Toughness", symbol="secret-vehicle-hit-points"),
    98: Jak3ItemData(item_id=98, name="Secret - Unlimited Vehicle Turbos", symbol="secret-unlimited-turbos"),
    99: Jak3ItemData(item_id=99, name="Secret - Toggle Jak's Goatee", symbol="secret-toggle-beard"),
    100: Jak3ItemData(item_id=100, name="Secret - Big Head Mode", symbol="secret-big-head"),
    101: Jak3ItemData(item_id=101, name="Secret - Small Head Mode", symbol="secret-little-head"),
    102: Jak3ItemData(item_id=102, name="Secret - Kleiver's Diaper", symbol="secret-kleever-diaper"),
    103: Jak3ItemData(item_id=103, name="Secret - Bad Weather", symbol="secret-bad-weather"),
    104: Jak3ItemData(item_id=104, name="Secret - Mirror World", symbol="secret-hflip-screen"),
    105: Jak3ItemData(item_id=105, name="Secret - Fast Movies", symbol="secret-fast-movie"),
    106: Jak3ItemData(item_id=106, name="Secret - Slow Movies", symbol="secret-slow-movie"),
    107: Jak3ItemData(item_id=107, name="Secret - Turbo JetBoard in Desert", symbol="secret-board-fast"),
    108: Jak3ItemData(item_id=108, name="Secret - Dark Jak Homing Attacks", symbol="secret-darkjak-tracking"),
    109: Jak3ItemData(item_id=109, name="Secret - Dark Jak Invisibility on Triangle Button",
                      symbol="secret-button-invis"),
    110: Jak3ItemData(item_id=110, name="Secret - Unlimited Ammo", symbol="secret-endless-ammo"),
    111: Jak3ItemData(item_id=111, name="Secret - Invulnerability", symbol="secret-invulnerable"),
    112: Jak3ItemData(item_id=112, name="Secret - Unlimited Dark Jak", symbol="secret-endless-dark"),
    113: Jak3ItemData(item_id=113, name="Secret - Unlimited Light Jak", symbol="secret-endless-light"),
}