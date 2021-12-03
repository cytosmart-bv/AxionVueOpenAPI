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
