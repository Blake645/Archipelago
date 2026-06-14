def spargus_to_desert(state, player) -> bool:
    return (
        state.has("Gate Pass to Spargus", player)
        and (
            state.has("Tough Puppy", player)
            or state.has("Sand Shark", player)
            or state.has("Gila Stomper", player)
            or state.has("Dune Hopper", player)
            or state.has("Slam Dozer", player)
            or state.has("Heat Seeker", player)
            or state.has("Dust Demon", player)
            or state.has("Desert Screamer", player)
        )
    )

def spargus_to_monk_temple(state, player) -> bool:
    return state.has_all("Gate Pass to Spargus", "Dune Hopper", player)


def spargus_to_nest(state, player) -> bool:
    return state.has_all("Gate Pass to Spargus", "Gila Stomper", player)


def spargus_to_port(state, player) -> bool:
    return state.has("Gate Pass to Spargus", "Air Train Pass", player)


def port_to_metal_head_section(state, player) -> bool:
    return state.has("Gate Pass to Spargus", "Air Train Pass", "Pass to Metal Head Section", player)


def port_to_inda(state, player) -> bool:
    return state.has("Gate Pass to Spargus", "Air Train Pass", "Pass to Industrial Section A", player)


def port_to_indb(state, player) -> bool:
    return state.has("Gate Pass to Spargus", "Air Train Pass", "Pass to Industrial Section A", "Pass to Industrial Section B",
                     player)


def port_to_hq(state, player) -> bool:
    return state.has("Gate Pass to Spargus", "Air Train Pass", "Pass to Industrial Section A",
                     "Pass to Industrial Section B", "Pass to Slums/New Haven",
                     player)

def port_to_ruins(state, player) -> bool:
    return state.has("Gate Pass to Spargus", "Air Train Pass", "Pass to Industrial Section A",
                     "Pass to Industrial Section B", "Pass to Slums/New Haven", "Pass to Outside Palace Ruins",
                     player)

def any_gun(state, player) -> bool:
    return state.has_any(("Scatter Gun", "Wave Concussor", "Plasmite RPG",
                          "Blaster", "Beam Reflexor", "Gyro Buster",
                          "Vulcan Fury", "Arc Wielder", "Needle Lazer",
                          "Peacemaker", "Mass Inverter", "Super Nova"), player)
