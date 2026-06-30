import json
import logging
import queue
import time
import struct
import random
from dataclasses import dataclass
from queue import Queue
from typing import Callable

import pymem
from pymem.exception import ProcessNotFound, ProcessError

import asyncio
from asyncio import StreamReader, StreamWriter, Lock

from NetUtils import NetworkItem
from ..items import item_table, Jak3ItemData, TRAP_ID_START, TRAP_ID_END

logger = logging.getLogger("Jak3ReplClient")


@dataclass
class JsonMessageData:
    my_item_name: str | None = None
    my_item_finder: str | None = None
    their_item_name: str | None = None
    their_item_owner: str | None = None


ALLOWED_CHARACTERS = frozenset({
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
    "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
    "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d",
    "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
    "o", "p", "q", "r", "s", "t", "u", "v", "w", "x",
    "y", "z", " ", "!", ":", ",", ".", "/", "?", "-",
    "=", "+", "'", "(", ")", "\""
})


class Jak3ReplClient:
    ip: str
    port: int
    reader: StreamReader
    writer: StreamWriter
    lock: Lock
    connected: bool = False
    initiated_connect: bool = False

    initial_item_count = -1
    received_initial_items = False
    processed_initial_items = False

    waiting_for_compile: bool = False
    compile_ready_time: float = 0.0

    gk_process: pymem.process = None
    goalc_process: pymem.process = None

    item_inbox: dict[int, NetworkItem] = {}
    inbox_index = 0
    json_message_queue: Queue[JsonMessageData] = queue.Queue()

    log_error: Callable
    log_warn: Callable
    log_success: Callable
    log_info: Callable

    def __init__(self,
                 log_error_callback: Callable,
                 log_warn_callback: Callable,
                 log_success_callback: Callable,
                 log_info_callback: Callable,
                 ip: str = "127.0.0.1",
                 port: int = 8181):
        self.ip = ip
        self.port = port
        self.lock = asyncio.Lock()
        self.log_error = log_error_callback
        self.log_warn = log_warn_callback
        self.log_success = log_success_callback
        self.log_info = log_info_callback

    async def main_tick(self):
        if self.initiated_connect:
            await self.connect()
            self.initiated_connect = False

        # Handle compile wait without blocking the event loop
        if self.waiting_for_compile:
            if asyncio.get_event_loop().time() >= self.compile_ready_time:
                self.waiting_for_compile = False
                self.log_info(logger, "[4/5] Set cheat mode to off...")
                await asyncio.sleep(0.5)
                await self.send_form_no_response("(set! *cheat-mode* #f)")
                await asyncio.sleep(0.5)
                self.log_info(logger, "[5/5] Run the title screen...")
                await self.send_form_no_response("(start 'play (get-continue-by-name *game-info* \"title-start\"))")
                self.log_success(logger, "The REPL is ready!")
                self.connected = True
            return

        if self.connected:
            try:
                self.gk_process.read_bool(self.gk_process.base_address)
            except ProcessError:
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
            try:
                self.goalc_process.read_bool(self.goalc_process.base_address)
            except ProcessError:
                msg = (f"Error sending data to compiler! (Did the compiler crash?)\n"
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

        if not self.processed_initial_items:
            if self.inbox_index >= self.initial_item_count >= 0:
                self.processed_initial_items = True
                await self.send_connection_status("ready")

        if len(self.item_inbox) > self.inbox_index:
            await self.receive_item()
            await self.save_data()
            self.inbox_index += 1

        if not self.json_message_queue.empty():
            json_txt_data = self.json_message_queue.get_nowait()
            await self.write_game_text(json_txt_data)

    async def send_form_no_response(self, form: str) -> bool:
        """Send a form that doesn't return a response through the socket."""
        header = struct.pack("<II", len(form), 10)
        async with self.lock:
            self.writer.write(header + form.encode())
            await self.writer.drain()
        return True

    async def send_form(self, form: str, print_ok: bool = True) -> bool:
        header = struct.pack("<II", len(form), 10)
        async with self.lock:
            self.writer.write(header + form.encode())
            await self.writer.drain()

            try:
                response_data = await asyncio.wait_for(self.reader.read(8192), timeout=120.0)
                response = response_data.decode()
            except asyncio.TimeoutError:
                self.log_error(logger, f"Timed out waiting for REPL response to: {form}")
                return False

            if response and len(response.strip()) > 0:
                if print_ok:
                    logger.debug(response)
                return True
            else:
                self.log_error(logger, f"Unexpected response from REPL: {response}")
                return False

    async def connect(self):
        try:
            self.gk_process = pymem.Pymem("gk.exe")
            logger.debug("Found the gk process: " + str(self.gk_process.process_id))
        except ProcessNotFound:
            self.log_error(logger, "Could not find the game process.")
            return

        try:
            self.goalc_process = pymem.Pymem("goalc.exe")
            logger.debug("Found the goalc process: " + str(self.goalc_process.process_id))
        except ProcessNotFound:
            self.log_error(logger, "Could not find the compiler process.")
            return

        try:
            self.reader, self.writer = await asyncio.open_connection(self.ip, self.port)
            await asyncio.sleep(1)
            connect_data = await self.reader.read(8192)
            welcome_message = connect_data.decode()

            if "Connected to OpenGOAL" and "nREPL!" in welcome_message:
                logger.debug(welcome_message)
            else:
                self.log_error(logger,
                               f"Unable to connect to REPL websocket: unexpected welcome message \"{welcome_message}\"")
        except ConnectionRefusedError as e:
            self.log_error(logger, f"Unable to connect to REPL websocket: {e.strerror}")
            return

        if self.reader and self.writer:
            self.log_info(logger, "[1/5] Listen on the game's port...")
            await asyncio.sleep(0.5)
            await self.send_form_no_response("(lt)")
            await asyncio.sleep(3)

            self.log_info(logger, "[2/5] Set debug flag to on...")
            await asyncio.sleep(0.5)
            await self.send_form_no_response("(set! *debug-segment* #t)")

            self.log_info(logger, "[3/5] Compile the game...")
            await asyncio.sleep(0.5)
            await self.send_form_no_response("(mi)")
            self.log_info(logger, "Waiting for compilation to finish (this may take a minute)...")
            self.waiting_for_compile = True
            self.compile_ready_time = asyncio.get_event_loop().time() + 30

    async def print_status(self):
        gc_proc_id = str(self.goalc_process.process_id) if self.goalc_process else "None"
        gk_proc_id = str(self.gk_process.process_id) if self.gk_process else "None"
        msg = (f"REPL Status:\n"
               f"   REPL process ID: {gc_proc_id}\n"
               f"   Game process ID: {gk_proc_id}\n")
        try:
            if self.reader and self.writer:
                addr = self.writer.get_extra_info("peername")
                addr = str(addr) if addr else "None"
                msg += f"   Game websocket: {addr}\n"
        except ConnectionResetError:
            msg += f"   Connection to the game was lost or reset!"
        last_item = str(getattr(self.item_inbox[self.inbox_index], "item")) if self.inbox_index else "None"
        msg += f"   Last item received: {last_item}\n"
        self.log_info(logger, msg)

    @staticmethod
    def sanitize_game_text(text: str) -> str:
        result = "".join([c if c in ALLOWED_CHARACTERS else "?" for c in text[:32]]).upper()
        result = result.replace("'", "\\c12")
        return f"\"{result}\""

    @staticmethod
    def sanitize_file_text(text: str) -> str:
        allowed_chars_no_extras = ALLOWED_CHARACTERS - {" ", "'", "(", ")", "\""}
        result = "".join([c if c in allowed_chars_no_extras else "" for c in text[:16]]).upper()
        return f"\"{result}\""

    def queue_game_text(self, my_item_name, my_item_finder, their_item_name, their_item_owner):
        pass

    async def write_game_text(self, data: JsonMessageData):
        logger.debug(f"Sending info to the in-game messenger!")
        body = ""
        if data.my_item_name and data.my_item_finder:
            body += (f" (append-messages (-> *ap-messenger* 0) \'recv "
                     f" {self.sanitize_game_text(data.my_item_name)} "
                     f" {self.sanitize_game_text(data.my_item_finder)})")
        if data.their_item_name and data.their_item_owner:
            body += (f" (append-messages (-> *ap-messenger* 0) \'sent "
                     f" {self.sanitize_game_text(data.their_item_name)} "
                     f" {self.sanitize_game_text(data.their_item_owner)})")
        await self.send_form_no_response(f"(begin {body} (none))")

    async def receive_item(self):
        item = getattr(self.item_inbox[self.inbox_index], "item")

        if item not in item_table:
            self.log_error(logger, f"Tried to receive item with unknown AP ID {item}!")
            return False

        item_data: Jak3ItemData = item_table[item]
        item_name: str = item_data.name
        item_symbol: str = item_data.symbol

        if TRAP_ID_START <= item <= TRAP_ID_END:
            ok = await self.send_form_no_response(f"(ap-trap-received! '{item_symbol})")
            logger.debug(f"Sent trap {item_name}!")
            return ok

        ok = await self.send_form_no_response(f"(ap-item-received! '{item_symbol})")
        if ok:
            logger.debug(f"Sent item {item_name}!")
        return ok

    async def setup_options(self,
                            slot_name: str,
                            slot_seed: str,
                            trap_time: int,
                            completion_type: int,
                            completion_value: int,
                            jak_is_jak2: int = 0) -> bool:
        sanitized_name = self.sanitize_file_text(slot_name)
        sanitized_seed = self.sanitize_file_text(slot_seed)

        ok = await self.send_form_no_response(f"(ap-setup-options! (new 'static 'ap-seed-options "
                                              f":slot-name {sanitized_name} "
                                              f":slot-seed {sanitized_seed} "
                                              f":trap-duration {trap_time}.0 "
                                              f":completion-type {completion_type} "
                                              f":completion-value {completion_value} "
                                              f":jak-is-jak2 {jak_is_jak2} ))")
        message = (f"Setting options: \n"
                   f"   Slot Name {sanitized_name}, \n"
                   f"   Slot Seed {sanitized_seed}, \n"
                   f"   Trap Duration {trap_time}, \n"
                   f"   Goal Type {completion_type}, \n"
                   f"   Goal Value {completion_value}, \n"
                   f"   Jak is Jak 2: {jak_is_jak2}... ")
        if ok:
            logger.debug(message + "Sent!")
        else:
            self.log_error(logger, message + "Failed!")
        return ok

    async def send_connection_status(self, status: str) -> bool:
        ok = await self.send_form_no_response(f"(ap-set-connection-status! (ap-connection-status {status}))")
        logger.debug(f"Connection Status {status} sent!")
        return ok

    async def save_data(self):
        with open("jak3_item_inbox.json", "w+") as f:
            dump = {
                "inbox_index": self.inbox_index,
                "item_inbox": [{
                    "item": self.item_inbox[k].item,
                    "location": self.item_inbox[k].location,
                    "player": self.item_inbox[k].player,
                    "flags": self.item_inbox[k].flags
                    } for k in self.item_inbox
                ]
            }
            json.dump(dump, f, indent=4)

    def load_data(self):
        try:
            with open("jak3_item_inbox.json", "r") as f:
                load = json.load(f)
                self.inbox_index = load["inbox_index"]
                self.item_inbox = {k: NetworkItem(
                        item=load["item_inbox"][k]["item"],
                        location=load["item_inbox"][k]["location"],
                        player=load["item_inbox"][k]["player"],
                        flags=load["item_inbox"][k]["flags"]
                    ) for k in range(0, len(load["item_inbox"]))
                }
        except FileNotFoundError:
            pass