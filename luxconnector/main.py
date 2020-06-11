#%%
import json
import os
import subprocess
import time
import uuid
from pathlib import Path
from typing import List

import cv2
import numpy as np
from websocket import create_connection


class LuxConnector:
    def __init__(self, zoom_type: str = "IN") -> None:
        self.__start_lux_app()
        self.ws = create_connection("ws://localhost:3333/luxservice")
        self.set_zoom(zoom_type)
        self.set_liveview(True)
        while True:
            try:
                img = self.get_image()
                if img is not None:
                    break
            except:
                pass
    
    def __activate(self) -> None:
        """
        Activate Lux
        """
        msg1 = {"type": "ACTIVATE", "payload": {}}
        self.ws.send(json.dumps(msg1))

    def __start_lux_app(self) -> None:
        """
        Run the Lux server in a subservers
        """
        print("Start Lux Server")
        basefolder_loc = Path(__file__).parents[0]
        exe_loc = os.path.join(basefolder_loc, "LuxServer", "CytoSmartLuxService.exe")
        subprocess.Popen(["cmd", "/K", exe_loc])

    def set_liveview(self, state: bool = True) -> None:
        """
        Turn the liveview on or off

        state: (bool) True = live view on
        """
        msg1 = {"type": "LIVE_STREAM", "payload": {"enable": state}}
        self.ws.send(json.dumps(msg1))

    def set_zoom(self, zoom_type: str = "IN") -> None:
        """
        Set zoom type by turning off or on binning.

        zoom_type: (bool) str = IN or OUT
        """
        zoom_type = zoom_type.upper()
        assert zoom_type in ["IN", "OUT"]

        msg1 = {"type": "ZOOM", "payload": {"action": zoom_type}}
        self.ws.send(json.dumps(msg1))

        # Toggle liveview to enforce the settings
        self.set_liveview(False)
        self.set_liveview(True)

    def set_focus(self, focus_level: float = 0) -> None:
        """
        Set the relative z-position of the camera.
        And with that the focus.

        focus_level: (float) between 0 and 1 where the camera need to be.
        """
        assert focus_level <= 1 and focus_level >= 0

        msg1 = {"type": "FOCUS", "payload": {"value": focus_level}}
        self.ws.send(json.dumps(msg1))

    def get_image(self) -> np.array:
        """
        Get the current image of the camera.
        """
        self.__activate()
        name = str(uuid.uuid4())
        msg1 = {
            "type": "EXPERIMENT",
            "payload": {
                "action": "START",
                "experimentId": "",
                "name": name,
                "snapshotInterval": 50,
                "autoStopTime": 1,
                "sasToken": "",
            },
        }

        self.ws.send(json.dumps(msg1))

        count = 0
        while True:
            try:
                load_location = os.path.join(
                    r"C:\ProgramData", "CytoSmartLuxService", "Images", name
                )

                all_img_names = [
                    i for i in os.listdir(load_location) if i.endswith(".jpg")
                ]

                img = cv2.imread(os.path.join(load_location, max(all_img_names)))

                assert img is not None
                break
            except:
                count += 1
                print(f"failed {count} times to load image from experiment")
                time.sleep(0.2)
                if count >= 50:
                    print(f"After trying {count} times it is still not working")
                    img = None
                    break

        msg2 = {
            "type": "EXPERIMENT",
            "payload": {
                "action": "STOP",
                "experimentId": "",
                "name": name,
                "snapshotInterval": 50,
                "autoStopTime": 1,
                "sasToken": "",
            },
        }

        self.ws.send(json.dumps(msg2))

        return img

    def get_z_stack(
        self, num_img: int = 10, start_focus: float = 0, stop_focus: float = 1
    ) -> List[np.array]:
        """
        Creates a z-stack.
        It will take multiple different image on different focus levels.

        num_img: (int) the amount of image in the z-stack
        start_focus: (float) The focus of the first image
        stop_focus: (float) the focus of the last image
        """
        
        result = []
        focus_step = (stop_focus - start_focus)/(num_img - 1)

        for focus_n in range(num_img):
            focus = start_focus + focus_n * focus_step
            focus = focus if focus <= 1 else 1

            print(f"focus level: {focus}")
            self.set_focus(focus)
            img = self.get_image()
            result.append(img)

        return result