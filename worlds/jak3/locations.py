from BaseClasses import Location
from .game_id import jak3_name
from .locs.mission_locations import get_max_mission_locations

class Jak3Location(Location):
    game: str = jak3_name

all_locations_table = get_max_mission_locations()