#%%
import json
import os
import subprocess
import time
import uuid
from io import BytesIO
from pathlib import Path
from typing import List

import requests
from PIL import Image
from websocket import create_connection

from .listener import Listener


class LuxConnector:
    def __init__(self, number_of_devices: int = 1) -> None:
        ''' 
        number_of_devices: (int) How many devices should be connected.
            It will keep trying connecting till it is connected to all connected devices.
        '''
        self.__start_lux_app()
        self.ws = create_connection("ws://localhost:3333/luxservice")
        self.ws_listener = Listener(self.ws)
        self.ws_listener.start()
        self.__all_devices = self.ws_listener.all_devices

        print(f"Connecting to {number_of_devices} devices")

        while True:
            try:
                connected_devices = 0
                all_serial_numbers = self.get_all_serial_numbers()
                for serial_number in all_serial_numbers:
                    img = self.get_image(serial_number)
                    if img is not None:
                        connected_devices += 1

                if connected_devices >= number_of_devices:
                    break
                
            except:
                pass

    def __activate(self, serial_number: str,) -> None:
        """
        Activate Lux

        serial_number: (str) the serial number of device you want to connect

        """
        msg1 = {"type": "ACTIVATE", "payload": {"serialNumber": serial_number}}
        self.ws.send(json.dumps(msg1))

    @staticmethod
    def __start_lux_app() -> None:
        """
        Run the Lux server in a subservers
        """
        print("Start Lux Server")
        basefolder_loc = Path(__file__).parents[0]
        exe_loc = os.path.join(basefolder_loc, "LuxServer", "CytoSmartLuxService.exe")
        subprocess.Popen(["cmd", "/K", exe_loc])

    def set_liveview(self, serial_number: str, state: bool = True) -> None:
        """
        Turn the liveview on or off

        serial_number: (str) the serial number of device you want to connect
        state: (bool) True = live view on
        """
        msg1 = {
            "type": "LIVE_STREAM",
            "payload": {"serialNumber": serial_number, "enable": state},
        }
        self.ws.send(json.dumps(msg1))

    def set_zoom(self, serial_number: str, zoom_type: str = "IN") -> None:
        """
        Set zoom type by turning off or on binning.

        serial_number: (str) the serial number of device you want to connect
        zoom_type: (bool) str = IN or OUT
        """
        zoom_type = zoom_type.upper()
        assert zoom_type in ["IN", "OUT"]

        msg1 = {
            "type": "ZOOM",
            "payload": {"serialNumber": serial_number, "action": zoom_type},
        }
        self.ws.send(json.dumps(msg1))

        # Toggle liveview to enforce the settings
        self.set_liveview(False)
        self.set_liveview(True)

    def set_focus(self, serial_number: str, focus_level: float = 0) -> None:
        """
        Set the relative z-position of the camera.
        And with that the focus.

        serial_number: (str) the serial number of device you want to connect
        focus_level: (float) between 0 and 1 where the camera need to be.
        """
        assert focus_level <= 1 and focus_level >= 0

        msg1 = {
            "type": "FOCUS",
            "payload": {"serialNumber": serial_number, "value": focus_level},
        }
        self.ws.send(json.dumps(msg1))

    def get_all_serial_numbers(self):
        """
        Returns all the serial numbers of the devices that are connected.
        """
        all_serial_numbers = []
        for serial_number in self.__all_devices.keys():
            device = self.__all_devices[serial_number]
            if device.is_connected:
                all_serial_numbers.append(serial_number)
        return all_serial_numbers
    
    def get_temperature(self, serial_number: str) -> float:
        """
        Returns the latest know temperature of the device.

        serial_number: (str) the serial number of device you want to connect
        """
        device = self.__all_devices[serial_number]
        return device.temperature

    def get_image(self, serial_number: str) -> Image.Image:
        """
        Get the current image of the camera.

        serial_number: (str) the serial number of device you want to connect
        """
        self.__activate(serial_number)
        self.set_liveview(serial_number, True)
        response = requests.get(
            f"http://localhost:3333/luxservice/lastlive?serialNumber={serial_number}"
        )
        img = Image.open(BytesIO(response.content))

        return img

    def get_z_stack(
        self,
        serial_number: str,
        num_img: int = 10,
        start_focus: float = 0,
        stop_focus: float = 1,
    ) -> List[Image.Image]:
        """
        Creates a z-stack.
        It will take multiple different image on different focus levels.

        serial_number: (str) the serial number of device you want to connect
        num_img: (int) the amount of image in the z-stack
        start_focus: (float) The focus of the first image
        stop_focus: (float) the focus of the last image
        """

        result = []
        focus_step = (stop_focus - start_focus) / (num_img - 1)

        for focus_n in range(num_img):
            focus = start_focus + focus_n * focus_step
            focus = focus if focus <= 1 else 1

            print(f"focus level: {focus}")
            self.set_focus(serial_number, focus)
            img = self.get_image(serial_number)
            result.append(img)

        return result
