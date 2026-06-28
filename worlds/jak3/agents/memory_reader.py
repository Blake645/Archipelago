import logging
import struct
from typing import ByteString, Callable
import json
import pymem
from pymem import pattern
from pymem.exception import ProcessNotFound, ProcessError, MemoryReadError, WinAPIError
from dataclasses import dataclass

from worlds.jak3.locs.mission_locations import main_tasks_to_missions, side_tasks_to_missions

logger = logging.getLogger("Jak3MemoryReader")


# Some helpful constants.
sizeof_uint64 = 8
sizeof_uint32 = 4
sizeof_uint8 = 1
sizeof_float = 4


# *****************************************************************************
# **** This number must match (-> *ap-info-jak3* version) in ap-struct.gc! ****
# *****************************************************************************
expected_memory_version = 4


@dataclass
class OffsetFactory:
    current_offset: int = 0

    def define(self, size: int, length: int = 1) -> int:
        bytes_to_alignment = self.current_offset % size
        if bytes_to_alignment != 0:
            self.current_offset += (size - bytes_to_alignment)
        offset_to_use = self.current_offset
        self.current_offset += (size * length)
        return offset_to_use


offsets = OffsetFactory()

memory_version_offset = offsets.define(sizeof_uint32)
next_mission_index_offset = offsets.define(sizeof_uint64)
next_side_mission_index_offset = offsets.define(sizeof_uint64)
missions_checked_offset = offsets.define(sizeof_uint32, 75)
side_missions_checked_offset = offsets.define(sizeof_uint32, 75)
connection_status_offset = offsets.define(sizeof_uint32)
slot_name_offset = offsets.define(sizeof_uint8, 16)
slot_seed_offset = offsets.define(sizeof_uint8, 8)
completion_goal_offset = offsets.define(sizeof_uint8)
completion_goal_type_offset = offsets.define(sizeof_uint32)
completion_goal_value_offset = offsets.define(sizeof_uint32)
completed_offset = offsets.define(sizeof_uint8)
death_count_offset = offsets.define(sizeof_uint32)
cause_of_death_offset = offsets.define(sizeof_uint8)
deathlink_enabled_offset = offsets.define(sizeof_uint8)
trap_duration_offset = offsets.define(sizeof_float)
end_marker_offset = offsets.define(sizeof_uint8, 4)


def as_float(value: int) -> int:
    return int(struct.unpack('f', value.to_bytes(sizeof_float, "little"))[0])


class Jak3MemoryReader:
    marker: ByteString
    goal_address: int | None = None
    connected: bool = False
    initiated_connect: bool = False

    gk_process: pymem.process = None

    location_outbox: list[int] = []
    outbox_index: int = 0
    finished_game: bool = False
    checks_per_mission: int = 1

    inform_checked_location: Callable
    inform_finished_game: Callable
    inform_died: Callable

    log_error: Callable
    log_warn: Callable
    log_success: Callable
    log_info: Callable

    def __init__(self,
                 location_check_callback: Callable,
                 finish_game_callback: Callable,
                 log_error_callback: Callable,
                 log_warn_callback: Callable,
                 log_success_callback: Callable,
                 log_info_callback: Callable,
                 marker: ByteString = b'ArChIpElAgO_JaK3\x00'):
        self.marker = marker

        self.inform_checked_location = location_check_callback
        self.inform_finished_game = finish_game_callback

        self.log_error = log_error_callback
        self.log_warn = log_warn_callback
        self.log_success = log_success_callback
        self.log_info = log_info_callback

    async def main_tick(self):
        if self.initiated_connect:
            await self.connect()
            self.initiated_connect = False

        if self.connected:
            try:
                self.gk_process.read_bool(self.gk_process.base_address)
            except (ProcessError, MemoryReadError, WinAPIError):
                msg = (f"Error reading game memory! (Did the game crash?)\n"
                       f"Please close all open windows and reopen the Jak 3 Client "
                       f"from the Archipelago Launcher.\n"
                       f"If the game and compiler do not restart automatically, please follow these steps:\n"
                       f"   Run the OpenGOAL Launcher, click Jak 3 > Features > Mods > ArchipelaGOAL.\n"
                       f"   Then click Advanced > Play in Debug Mode.\n"
                       f"   Then click Advanced > Open REPL.\n"
                       f"   Then close and reopen the Jak 3 Client from the Archipelago Launcher.")
                self.log_error(logger, msg)
                self.connected = False
        else:
            return

        if self.connected:
            self.read_memory()

            if len(self.location_outbox) > self.outbox_index:
                self.inform_checked_location(self.location_outbox)
                self.save_data()
                self.outbox_index += 1

            if self.finished_game:
                self.inform_finished_game()

    async def connect(self):
        try:
            self.gk_process = pymem.Pymem("gk.exe")
            logger.debug("Found the gk process: " + str(self.gk_process.process_id))
        except ProcessNotFound:
            self.log_error(logger, "Could not find the game process.")
            self.connected = False
            return

        modules = list(self.gk_process.list_modules())
        logger.debug(f"Found {len(modules)} modules to search through.")
        for i, module in enumerate(modules):
            marker_address = pattern.pattern_scan_module(self.gk_process.process_handle, module, self.marker)
            if marker_address:
                goal_pointer = marker_address + len(self.marker) + 7
                self.goal_address = int.from_bytes(self.gk_process.read_bytes(goal_pointer, sizeof_uint64),
                                                   byteorder="little",
                                                   signed=False)
                logger.debug("Found the archipelago memory address: " + str(self.goal_address))
                await self.verify_memory_version()
                break
            else:
                self.log_warn(logger, f"Could not find the Archipelago marker address in module {i}, continuing...")
        else:
            self.log_warn(logger, f"Could not find the Archipelago marker address in any module!")
            self.connected = False

    async def verify_memory_version(self):
        if self.goal_address is None:
            self.log_error(logger, "Could not find the Archipelago memory address!")
            self.connected = False
            return

        memory_version: int | None = None
        try:
            memory_version = self.read_goal_address(memory_version_offset, sizeof_uint32)
            if memory_version == expected_memory_version:
                self.log_success(logger, "The Memory Reader is ready!")
                self.connected = True
            else:
                raise MemoryReadError(memory_version_offset, sizeof_uint32)
        except (ProcessError, MemoryReadError, WinAPIError):
            if memory_version is None:
                msg = (f"Could not find a version number in the OpenGOAL memory structure!\n"
                       f"   Expected Version: {str(expected_memory_version)}\n"
                       f"   Found Version: {str(memory_version)}\n"
                       f"Please follow these steps:\n"
                       f"   If the game is running, try entering '/memr connect' in the client.\n"
                       f"   You should see 'The Memory Reader is ready!'\n"
                       f"   If that did not work, or the game is not running, run the OpenGOAL Launcher.\n"
                       f"   Click Jak 3 > Features > Mods > ArchipelaGOAL.\n"
                       f"   Then click Advanced > Play in Debug Mode.\n"
                       f"   Try entering '/memr connect' in the client again.")
            else:
                msg = (f"The OpenGOAL memory structure is incompatible with the current Archipelago client!\n"
                       f"   Expected Version: {str(expected_memory_version)}\n"
                       f"   Found Version: {str(memory_version)}\n"
                       f"Please follow these steps:\n"
                       f"   Run the OpenGOAL Launcher, click Jak 3 > Features > Mods > ArchipelaGOAL.\n"
                       f"   Click Update (if one is available).\n"
                       f"   Click Advanced > Compile. When this is done, click Continue.\n"
                       f"   Click Versions and verify the latest version is marked 'Active'.\n"
                       f"   Close all launchers, games, clients, and console windows, then restart Archipelago.")
            self.log_error(logger, msg)
            self.connected = False

    async def print_status(self):
        proc_id = str(self.gk_process.process_id) if self.gk_process else "None"
        last_loc = str(self.location_outbox[self.outbox_index - 1] if self.outbox_index else "None")
        msg = (f"Memory Reader Status:\n"
               f"   Game process ID: {proc_id}\n"
               f"   Game state memory address: {str(self.goal_address)}\n"
               f"   Last location checked: {last_loc}\n"
               f"   Checks per mission: {self.checks_per_mission}")
        await self.verify_memory_version()
        self.log_info(logger, msg)

    def read_memory(self) -> list[int]:
        try:
            next_mission_idx = self.read_goal_address(next_mission_index_offset, sizeof_uint64)
            for i in range(int(next_mission_idx)):
                raw_main_task_id = self.read_goal_address(missions_checked_offset + (i * sizeof_uint32),
                                                          sizeof_uint32)

                if raw_main_task_id in main_tasks_to_missions:
                    main_mission_id = main_tasks_to_missions[raw_main_task_id].mission_id
                    mission_name = main_tasks_to_missions[raw_main_task_id].name

                    for check in range(1, self.checks_per_mission + 1):
                        loc_id = main_mission_id * 100 + check
                        if loc_id not in self.location_outbox:
                            self.location_outbox.append(loc_id)
                            logger.debug(f"Mission completed! Raw game-task: {raw_main_task_id}"
                                         f" -> Mission ID: {main_mission_id}"
                                         f" -> Check {check}"
                                         f" -> Location ID: {loc_id}"
                                         f" -> '{mission_name}'")

            next_side_mission_idx = self.read_goal_address(next_side_mission_index_offset, sizeof_uint64)
            for i in range(int(next_side_mission_idx)):
                raw_side_task_id = self.read_goal_address(side_missions_checked_offset + (i * sizeof_uint32),
                                                          sizeof_uint32)

                if raw_side_task_id in side_tasks_to_missions:
                    side_mission_id = side_tasks_to_missions[raw_side_task_id].mission_id
                    side_mission_name = side_tasks_to_missions[raw_side_task_id].name

                    for check in range(1, self.checks_per_mission + 1):
                        loc_id = side_mission_id * 100 + check
                        if loc_id not in self.location_outbox:
                            self.location_outbox.append(loc_id)
                            logger.debug(f"Side mission completed! Raw game-task: {raw_side_task_id}"
                                         f" -> Mission ID: {side_mission_id}"
                                         f" -> Check {check}"
                                         f" -> Location ID: {loc_id}"
                                         f" -> '{side_mission_name}'")

            completed = self.read_goal_address(completed_offset, sizeof_uint8)
            if completed > 0 and not self.finished_game:
                self.finished_game = True
                self.log_success(logger, "Congratulations! You finished the game!")

        except (ProcessError, MemoryReadError, WinAPIError):
            msg = (f"Error reading game memory! (Did the game crash?)\n"
                   f"Please close all open windows and reopen the Jak 3 Client "
                   f"from the Archipelago Launcher.\n"
                   f"If the game and compiler do not restart automatically, please follow these steps:\n"
                   f"   Run the OpenGOAL Launcher, click Jak 3 > Features > Mods > ArchipelaGOAL.\n"
                   f"   Then click Advanced > Play in Debug Mode.\n"
                   f"   Then click Advanced > Open REPL.\n"
                   f"   Then close and reopen the Jak 3 Client from the Archipelago Launcher.")
            self.log_error(logger, msg)
            self.connected = False

        return self.location_outbox

    def read_goal_address(self, offset: int, length: int) -> int:
        return int.from_bytes(
            self.gk_process.read_bytes(self.goal_address + offset, length),
            byteorder="little",
            signed=False)

    def save_data(self):
        with open("jak3_location_outbox.json", "w+") as f:
            dump = {
                "outbox_index": self.outbox_index,
                "location_outbox": self.location_outbox
            }
            json.dump(dump, f, indent=4)

    def load_data(self):
        try:
            with open("jak3_location_outbox.json", "r") as f:
                load = json.load(f)
                self.outbox_index = load["outbox_index"]
                self.location_outbox = load["location_outbox"]
        except FileNotFoundError:
            pass