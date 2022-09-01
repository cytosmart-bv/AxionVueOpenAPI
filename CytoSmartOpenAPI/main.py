#%%
import json
import os
import subprocess
from io import BytesIO
from pathlib import Path
import time
from typing import List, Tuple
import webbrowser

import requests
from PIL import Image
from websocket import create_connection

from .listener import Listener


class CytoSmartOpenAPI:
    def __init__(self, number_of_devices: int = 1, *, warranty: bool) -> None:
        """
        number_of_devices: (int) How many devices should be connected.
            It will keep trying to connect till it is connected to all connected devices.
        warranty: (bool) ⚠️ When using the openAPI you are voiding the hardware warranty
        """
        if warranty:
            raise ValueError("The warranty MUST be set to False")
        self.__connect_with_service()
        self.ws_listener = Listener(self.__recv_ws_message)
        self.ws_listener.start()
        self.__all_devices = self.ws_listener.all_devices
        assert (
            number_of_devices >= 1
        ), f"number_of_devices needs to be above 1, not {number_of_devices}"
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

    def __connect_with_service(self):
        """
        Try to connect with CytoSmartService websocket instance.
        If that does not work, start a instants of the service
        """
        try:
            # Try to make a connection with the app
            self.ws = create_connection("ws://localhost:3333/cytosmartservice")
        except:
            # If that fails, start the app first and make the connection again
            self.__start_cytosmart_app()
            self.ws = create_connection("ws://localhost:3333/cytosmartservice")

    def __send_ws_message(self, msg: dict, count: int = 0):
        """Send a message to the service.
        It will retry if the connection got lost after restoring the connection

        Args:
            msg (dict): Message itself needs to have type and payload
            count (int, optional): Number of times trying. Defaults to 0.

        Raises:
            RecursionError: If a 100 times is not enough to send the message, give up
        """
        if count == 100:
            raise RecursionError(f"Retried to send a message {count} times")
        try:
            self.ws.send(json.dumps(msg))
        except ConnectionResetError:
            print(f"Connection lost, reconnecting. Attempt {count}")
            self.__connect_with_service()
            self.__send_ws_message(msg, count + 1)

    def __recv_ws_message(self, count: int = 0):
        """Receive a message to the service.
        It will retry if the connection got lost after restoring the connection

        Args:
            count (int, optional): Number of times trying. Defaults to 0.

        Raises:
            RecursionError: If a 100 times is not enough to recieve the message, give up
        """
        if count == 100:
            raise RecursionError(f"Retried to receive a message {count} times")

        try:
            return json.loads(self.ws.recv())
        except ConnectionResetError:
            print(f"Connection lost, reconnecting. Attempt {count}")
            self.__connect_with_service()
            self.__recv_ws_message(count + 1)

    def __activate(
        self,
        serial_number: str,
    ) -> None:
        """
        Activate device

        serial_number: (str) the serial number of device you want to connect

        """
        self.__send_ws_message(
            {"type": "ACTIVATE", "payload": {"serialNumber": serial_number}}
        )

    @staticmethod
    def __start_cytosmart_app() -> None:
        """
        Run the cytosmart server in a subprocess
        """
        print("Start CytoSMART Server")
        basefolder_loc = Path(__file__).parents[0]
        exe_loc = os.path.join(basefolder_loc, "CytoSmartApp", "CytoSmartService.exe")
        subprocess.Popen(["cmd", "/K", exe_loc])

    def do_autofocus(
        self, serial_number: str, chamber_type: str, max_waiting_time: float = 60
    ) -> None:
        """
        Turn the liveview on or off

        serial_number: (str) the serial number of device you want to connect
        chamber_type: (str)
            other (SLOW) -> the device will go through its whole range of motion.
            csslide(FAST) -> the device will go through limited range of motion where the cells are expected to be.
            slide (FAST) -> the device will go through limited range of motion where the cells are expected to be.
        max_waiting_time (float, optional): Maximum time it waits for the stage to arrive.
            If it is set to -1 it will never timeout
            Defaults to 60.
        """
        if chamber_type.lower() == "other":
            chamber_type_number = 0
        elif chamber_type.lower() == "csslide":
            chamber_type_number = 1
        elif chamber_type.lower() == "slide":
            chamber_type_number = 2
        else:
            raise ValueError(f"Chamber type {chamber_type} is not supported")

        # Get device and set autofocus to True before starting
        # This prefents reading False before the device replied with the first True
        device = self.__all_devices[serial_number]
        device.is_auto_focusing = True

        self.__send_ws_message(
            {
                "type": "AUTOFOCUS",
                "payload": {
                    "action": "START",
                    "serialNumber": serial_number,
                    "chamberType": chamber_type_number,
                },
            }
        )

        start_time = time.time()
        while device.is_auto_focusing:
            # Time out check
            current_waiting_time = time.time() - start_time
            if current_waiting_time > max_waiting_time and max_waiting_time > 0:
                raise TimeoutError(
                    f"""
                    Auto focusing took too long. It took {current_waiting_time}, max is {max_waiting_time}. 
                    """
                )

            # To not spam the service wait a bit
            time.sleep(0.1)

    def set_liveview(self, serial_number: str, state: bool = True) -> None:
        """
        Turn the liveview on or off

        serial_number: (str) the serial number of device you want to connect
        state: (bool) True = live view on
        """
        self.__send_ws_message(
            {
                "type": "LIVE_STREAM",
                "payload": {"serialNumber": serial_number, "enable": state},
            }
        )

    def open_liveview(self, serial_number: str) -> None:
        """
        Open the live view in the browser

        serial_number: (str) the serial number of device you want to connect
        """
        webbrowser.open(
            f"http://localhost:3333/cytosmartservice/live?serialNumber={serial_number}"
        )

    def set_zoom(self, serial_number: str, zoom_type: str = "IN") -> None:
        """
        Set zoom type by turning off or on binning.

        serial_number: (str) the serial number of device you want to connect
        zoom_type: (bool) str = IN or OUT
        """
        zoom_type = zoom_type.upper()
        assert zoom_type in [
            "IN",
            "OUT",
        ], f"zoom type needs to be IN or OUT not {zoom_type}"

        self.__send_ws_message(
            {
                "type": "ZOOM",
                "payload": {"serialNumber": serial_number, "action": zoom_type},
            }
        )

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
        assert (
            focus_level <= 1 and focus_level >= 0
        ), f"Focus level needs to be between 0 and 1, not {focus_level}"

        current_channel = self.__all_devices[serial_number].active_channel
        self.__set_active_camera(serial_number, "BRIGHTFIELD")
        self.__send_ws_message(
            {
                "type": "FOCUS",
                "payload": {"serialNumber": serial_number, "value": focus_level},
            }
        )
        print("current_channel", current_channel)
        self.__set_active_camera(serial_number, current_channel)
        # Give device time to go to new focus
        if current_channel == "BRIGHTFIELD":
            time.sleep(0.5)
        else:
            time.sleep(2)

    def set_active_camera(
        self,
        serial_number: str,
        color_channel: str = "BRIGHTFIELD",
        max_waiting_time: float = 10,
    ) -> None:
        """
        Set a camera to active.
        You can switch between brightfield, red fluo, and green fluo
        This is only for fluo devices

        serial_number: (str) the serial number of device you want to connect
        focus_level: (float) between 0 and 1 where the camera needs to be.
        color_channel: (str) The camera you want to change the setting of.
            options: "BRIGHTFIELD", "RED", "GREEN"
            Default: "BRIGHTFIELD"
        max_waiting_time (float, optional): Maximum time it waits for the stage to arrive.
                If it is set to -1 it will never timeout
                Defaults to 10.
        """
        color_channel = color_channel.upper()
        assert color_channel in [
            "BRIGHTFIELD",
            "RED",
            "GREEN",
        ], f"color_channel needs to be BRIGHTFIELD, RED, or GREEN not {color_channel}"
        self.__set_active_camera(
            serial_number, color_channel, max_waiting_time=max_waiting_time
        )

    def __set_active_camera(
        self,
        serial_number: str,
        color_channel: str = "BRIGHTFIELD",
        max_waiting_time: float = 60,
    ) -> None:
        device = self.__all_devices[serial_number]
        if device.active_channel == color_channel:
            return
        self.__send_ws_message(
            {
                "type": "COLOR_CHANNEL",
                "payload": {
                    "serialNumber": serial_number,
                    "colorChannel": color_channel,
                },
            }
        )

        start_time = time.time()
        while True:
            if device.active_channel == color_channel:
                return
            time.sleep(0.1)
            current_waiting_time = time.time() - start_time
            if current_waiting_time > max_waiting_time and max_waiting_time > 0:
                raise TimeoutError(
                    f"""
                    Changing the channel took too long. It took {current_waiting_time}, max is {max_waiting_time}. 
                    """
                )

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
            If focus is set to 0.4 and focus_offset for RED is set to 0.1 RED focus is 0.5 (Fluo only)
        """
        color_channel = color_channel.upper()
        assert color_channel in [
            "BRIGHTFIELD",
            "RED",
            "GREEN",
        ], f"color_channel needs to be BRIGHTFIELD, RED, or GREEN not {color_channel}"
        if color_channel == "BRIGHTFIELD":
            assert (
                0 < exposure and exposure <= 10
            ), f"exposure for BRIGHTFIELD needs to be between 0 and 10, not {exposure}"
        else:
            assert (
                0 < exposure and exposure <= 8000
            ), f"exposure for RED, or GREEN needs to be between 0 and 8000, not {exposure}"
        assert (
            0 < gain and gain < 100
        ), f"gain needs to be between 0 and 100, not {gain}"
        assert (
            0 < brightness and brightness <= 10000
        ), f"brightness needs to be between 0 and 10000, not {brightness}"

        # Turn on live stream and wait till it is one
        device = self.__all_devices[serial_number]

        self.set_liveview(serial_number, True)

        while device.live_stream == False:
            pass

        self.__send_ws_message(
            {
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
        )

    def set_flash_duration(self, serial_number: str, duration: int) -> None:
        """
        Setting the time in μs the led is on during the taking of a picture.

        Args:
        serial_number: (str) the serial number of device you want to connect
            duration (int): μs between 40 and 250
        """
        assert (
            40 <= duration and duration <= 250
        ), f"Duration needs to be between 40 and 250 μs, not {duration}"
        self.__send_ws_message(
            {
                "type": "OMNI_SET_FLASH_DURATION",
                "payload": {"serialNumber": serial_number, "duration": duration},
            }
        )

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

    def move_stage(
        self,
        serial_number: str,
        new_x: float,
        new_y: float,
        max_waiting_time: float = 60,
    ) -> None:
        """
        Moves the stage the the new position (Omni only)

        Args:
            serial_number: (str) the serial number of device you want to connect
            new_x (float): new x position in millimeters
            new_y (float): new y position in millimeters
            max_waiting_time (float, optional): Maximum time it waits for the stage to arrive.
                If it is set to -1 it will never timeout
                Defaults to 60.

        Raises:
            TimeoutError: Stage took longer then the max_waiting_time to go to new position
        """

        msg = {
            "type": "OMNI_MOVE_STAGE",
            "payload": {
                "serialNumber": serial_number,
                "X": float(new_x),
                "Y": float(new_y),
            },
        }
        self.__send_ws_message(msg)

        start_time = time.time()
        device = self.__all_devices[serial_number]
        while True:
            cur_x, cur_y = self.get_position(serial_number)
            is_moving = device.is_moving

            # If the device is not moving AND close enough stop
            if (
                abs(cur_x - new_x) < 0.1
                and abs(cur_y - new_y) < 0.1
                and is_moving == False
            ):
                break
            # If it is only not move but still not close send the message again
            elif is_moving == False:
                self.__send_ws_message(msg)

            # Time out check
            current_waiting_time = time.time() - start_time
            if current_waiting_time > max_waiting_time and max_waiting_time > 0:
                raise TimeoutError(
                    f"""
                    Moving stage took too long. It took {current_waiting_time}, max is {max_waiting_time}. 
                    Current state:
                    Position: {cur_x}, {cur_y}
                    Is_moving: {is_moving}
                    Wanted position: {new_x}, {new_y}
                    """
                )

            # To not spam the service wait a bit
            time.sleep(0.5)

    def get_position(self, serial_number: str) -> Tuple[float, float]:
        """
        Returns the latest known position of the device.

        serial_number: (str) the serial number of device you want to connect
        """

        self.__send_ws_message(
            {
                "type": "OMNI_REQUEST_STAGE_POSITION",
                "payload": {"serialNumber": serial_number},
            }
        )
        time.sleep(0.1)
        device = self.__all_devices[serial_number]
        if device.is_sleeping:
            return -1, -1
        return device.x, device.y

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
        It will take multiple different images on different focus levels.

        serial_number: (str) the serial number of device you want to connect
        num_img: (int) the amount of images in the z-stack
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
