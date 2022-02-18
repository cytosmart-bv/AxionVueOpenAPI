#%%
import json
import os
import subprocess
from io import BytesIO
from pathlib import Path
import time
from typing import List

import requests
from PIL import Image
from websocket import create_connection

from .listener import Listener


class LuxConnector:
    def __init__(self, number_of_devices: int = 1) -> None:
        """
        number_of_devices: (int) How many devices should be connected.
            It will keep trying connecting till it is connected to all connected devices.
        """

        try:
            # Try to make a connection with the app
            self.ws = create_connection("ws://localhost:3333/cytosmartservice")
        except:
            # If that fails, start the app first and make the connection again
            self.__start_lux_app()
            self.ws = create_connection("ws://localhost:3333/cytosmartservice")
        self.ws_listener = Listener(self.ws)
        self.ws_listener.start()
        self.__all_devices = self.ws_listener.all_devices
        self.active_camera = "BRIGHTFIELD"
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

    def __activate(
        self,
        serial_number: str,
    ) -> None:
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
        exe_loc = os.path.join(basefolder_loc, "LuxServer", "CytoSmartService.exe")
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
        self.set_liveview(serial_number, False)
        self.set_liveview(serial_number, True)

    def set_focus(self, serial_number: str, focus_level: float = 0) -> None:
        """
        Set the relative z-position of the camera.
        And with that the focus.

        serial_number: (str) the serial number of device you want to connect
        focus_level: (float) between 0 and 1 where the camera need to be.
        """
        assert focus_level <= 1 and focus_level >= 0

        self.__set_active_camera(serial_number, "BRIGHTFIELD")
        msg1 = {
            "type": "FOCUS",
            "payload": {"serialNumber": serial_number, "value": focus_level},
        }
        self.ws.send(json.dumps(msg1))
        self.__set_active_camera(serial_number, self.active_camera)
        # Give device time to go to new focus
        if self.active_camera == "BRIGHTFIELD":
            time.sleep(0.5)
        else:
            time.sleep(2)

    def set_active_camera(
        self, serial_number: str, color_channel: str = "BRIGHTFIELD"
    ) -> None:
        """
        Set a camera to active.
        You can switch between brightfield, red fluo, and green fluo
        This is only for fluo devices

        serial_number: (str) the serial number of device you want to connect
        focus_level: (float) between 0 and 1 where the camera need to be.
        color_channel: (str) The camera you want to change the setting of.
            options: "BRIGHTFIELD", "RED", "GREEN"
            Default: "BRIGHTFIELD"
        """
        color_channel = color_channel.upper()
        assert color_channel in ["BRIGHTFIELD", "RED", "GREEN"]
        self.active_camera = color_channel
        self.__set_active_camera(serial_number, color_channel)
    
    def __set_active_camera(self, serial_number: str, color_channel: str = "BRIGHTFIELD"
    ) -> None:
        msg1 = {
            "type": "COLOR_CHANNEL",
            "payload": {"serialNumber": serial_number, "colorChannel": color_channel},
        }
        self.ws.send(json.dumps(msg1))

    def set_camera_settings(
        self,
        serial_number: str,
        color_channel: str = "BRIGHTFIELD",
        exposure: float = 10,
        gain: int = 20,
        brightness: int = 7500,
        focus_offset: float = 0.0,
    ) -> None:
        """
        Change the camera settings for 1 camera of 1 device.
        Brightfield devices have 1 camera; BRIGHTFIELD
        Fluo device have 3; BRIGHTFIELD, RED, and GREEN

        WARNING: This only changes settings of the camera,
            it does NOT activate it.
            Use set_active_camera to activate the camera you need.

        serial_number: (str) the serial number of device you want to connect
        exposure: (float) The time in milliseconds the camera is detecting light.
        gain: (int) The multiplication of the camera. (Fluo only)
            If very little light goes into the camera sensor make sure the gain is high.
        brightness: (int) Strength of the led when it is on (Fluo only)
        color_channel: (str) The camera you want to change the setting of.
            options: "BRIGHTFIELD", "RED", "GREEN"
            Default: "BRIGHTFIELD"
        focus_offset: (float) the difference in focus between brightfield and fluo.
            If focus is set to 0.4 and focus_offset for RED is set to 0.1 RED focus is 0.5
        """
        color_channel = color_channel.upper()
        assert color_channel in ["BRIGHTFIELD", "RED", "GREEN"]
        if color_channel == "BRIGHTFIELD":
            assert 0 < exposure and exposure <= 10
        else:
            assert 0 < exposure and exposure <= 8000
        assert 0 < gain and gain < 100
        assert 0 < brightness and brightness <= 10000

        msg1 = {
            "type": "CAMERA_SETTINGS",
            "payload": {
                "serialNumber": serial_number,
                "gain": gain,
                "exposure": exposure,
                "colorChannel": color_channel,
                "brightness": brightness,
                "focusOffset": focus_offset,
            },
        }

        # Turn on live stream and wait till it is one
        device = self.__all_devices[serial_number]

        self.set_liveview(serial_number, True)

        while device.live_stream == False:
            pass

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
            f"http://localhost:3333/cytosmartservice/lastlive?serialNumber={serial_number}"
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
