#%%
import json
import time
from threading import Thread
from typing import Dict

import websocket

from .lux_device import LuxDevice


class Listener(Thread):
    def __init__(self, ws: websocket.WebSocket):
        Thread.__init__(self)
        self.ws = ws
        self.daemon = True
        self.last_msg = None
        self.all_devices: Dict[str, LuxDevice] = {}
        self.x = -1.
        self.y = -1.
    def run(self):
        while True:
            new_message = json.loads(self.ws.recv())
            self.last_msg = new_message

            type_message = new_message.get("type", "")
            payload = new_message.get("payload", {})
            serial_number = payload.get("serialNumber", "")

            if type_message == "DEVICE_CHANGE":
                isConnected = bool(payload.get("isConnected", False))
                self.__connect_device(serial_number, isConnected)

            if type_message == "TEMPERATURE_CHANGE":
                new_temperature = float(payload.get("value", -9999999))
                self.__update_temperature(serial_number, new_temperature)

            if type_message == "LIVE_STREAM_CHANGE":
                new_live_stream = bool(payload.get("isEnabled", -9999999))
                self.__update_live_stream(serial_number, new_live_stream)

            if type_message == "OMNI_MOVE_STAGE_CHANGE":
                new_x = float(payload.get("x", -1.))
                new_y = float(payload.get("y", -1.))
                self.__update_position(serial_number, new_x, new_y)

            if type_message == "SLEEP_CHANGE":
                is_sleeping = float(payload.get("isSleeping", True))
                self.__update_sleep(serial_number, is_sleeping)

    def __connect_device(self, serial_number: str, is_connected: bool = True):
        device = self.all_devices.get(serial_number, None)
        if device is None:
            self.all_devices[serial_number] = LuxDevice(
                serial_number, is_connected=is_connected
            )
        else:
            self.all_devices[serial_number].is_connected = is_connected

    def __update_temperature(self, serial_number: str, new_temperature: float):
        device = self.all_devices.get(serial_number, None)
        if device is not None:
            device.temperature = new_temperature

    def __update_live_stream(self, serial_number: str, new_live_stream: float):
        device = self.all_devices.get(serial_number, None)
        if device is not None:
            device.live_stream = new_live_stream

    def __update_position(self, serial_number: str, x: float, y: float):
        device = self.all_devices.get(serial_number, None)
        if device is not None:
            device.x = x
            device.y = y

    def __update_sleep(self, serial_number, is_sleeping):
        device = self.all_devices.get(serial_number, None)
        if device is not None:
            device.is_sleeping = is_sleeping