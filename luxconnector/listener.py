#%%
import json
from threading import Thread
import time
import websocket
from .lux_device import LuxDevice

class Listener(Thread):

    def __init__(self, ws: websocket.WebSocket):
        Thread.__init__(self)
        self.ws = ws
        self.daemon = True
        self.last_msg = None
        self.all_devices = {}
    
    def run(self):
        while True:
            new_message =  json.loads(self.ws.recv())
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
        
# l = Listener(websocket.create_connection("ws://localhost:3333/luxservice"))
# l.start()
# print(l.last_msg)