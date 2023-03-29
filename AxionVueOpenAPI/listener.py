#%%
from threading import Thread
import time
from typing import Dict, Callable

from .axion_vue_device import AxionVueDevice


class Listener(Thread):
    """Listens to the websocket for changes.
    Once a change occurs it will update the correct device based on serial number
    """

    def __init__(self, receive_function: Callable):
        Thread.__init__(self)
        self.receive_function = receive_function
        self.daemon = True
        self.all_devices: Dict[str, AxionVueDevice] = {}

    def run(self):
        while True:
            new_message = self.receive_function()
            if new_message == None:
                time.sleep(0.5)
                continue
            type_message = new_message.get("type", "")
            payload = new_message.get("payload", {})
            serial_number = payload.get("serialNumber", "")

            if type_message == "DEVICE_CHANGE":
                _is_connected = bool(payload.get("isConnected", False))
                self.__connect_device(serial_number, _is_connected)
                continue

            if type_message == "TEMPERATURE_CHANGE":
                _temperature = float(payload.get("value", -9999999))
                self.__update_temperature(serial_number, _temperature)
                continue

            if type_message == "LIVE_STREAM_CHANGE":
                _live_stream = bool(payload.get("isEnabled", -9999999))
                self.__update_live_stream(serial_number, _live_stream)
                continue

            if type_message == "OMNI_MOVE_STAGE_CHANGE":
                _x = float(payload.get("x", -1.0))
                _y = float(payload.get("y", -1.0))
                _state = payload.get("state")
                self.__update_position(serial_number, _x, _y)
                self.__update_is_moving(serial_number, _state)
                continue

            if type_message == "SLEEP_CHANGE":
                _is_sleeping = float(payload.get("isSleeping", True))
                self.__update_sleep(serial_number, _is_sleeping)
                continue

            if type_message == "AUTOFOCUS_CHANGE":
                _is_auto_focusing = payload.get("isAutoFocusing", "Not found")
                self.__update_auto_focusing(serial_number, _is_auto_focusing)
                continue

            if type_message == "COLOR_CHANNEL_CHANGE":
                _new_channel = payload.get("colorChannel", "")
                self.__update_active_channel(serial_number, _new_channel)

    def __connect_device(self, serial_number: str, is_connected: bool = True):
        device = self.all_devices.get(serial_number, None)
        if device is None:
            self.all_devices[serial_number] = AxionVueDevice(
                serial_number, is_connected=is_connected
            )
        else:
            self.all_devices[serial_number].is_connected = is_connected

    def __update_temperature(self, serial_number: str, new_temperature: float):
        device = self.all_devices.get(serial_number, None)
        if device:
            device.temperature = new_temperature

    def __update_live_stream(self, serial_number: str, new_live_stream: float):
        device = self.all_devices.get(serial_number, None)
        if device:
            device.live_stream = new_live_stream

    def __update_position(self, serial_number: str, x: float, y: float):
        device = self.all_devices.get(serial_number, None)
        if device:
            device.x = x
            device.y = y

    def __update_is_moving(self, serial_number: str, is_moving_state: bool):
        device = self.all_devices.get(serial_number, None)
        if device:
            if is_moving_state in ["False"]:
                device.is_moving = False
            if is_moving_state in ["True"]:
                device.is_moving = True

    def __update_sleep(self, serial_number, is_sleeping):
        device = self.all_devices.get(serial_number, None)
        if device:
            device.is_sleeping = is_sleeping

    def __update_active_channel(self, serial_number, new_channel: str):
        device = self.all_devices.get(serial_number, None)
        if device:
            device.active_channel = new_channel

    def __update_auto_focusing(self, serial_number, _is_auto_focusing):
        device = self.all_devices.get(serial_number, None)
        if device:
            if _is_auto_focusing in ["True", "true", True]:
                device.is_auto_focusing = True
            else:
                device.is_auto_focusing = False
