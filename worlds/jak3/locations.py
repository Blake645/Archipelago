from BaseClasses import Location
from .game_id import jak3_name
from .locs import (mission_locations as missions)


class Jak3Location(Location):
    game: str = jak3_name


all_locations_table = {
    **{k: v for k, v in missions.main_mission_table.items()},
    **{k: v for k, v in missions.side_mission_table.items()}
}
