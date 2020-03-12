#%%
import json
import os
import subprocess
import time
import uuid
from pathlib import Path

from PIL import Image
from websocket import create_connection


class LuxConnector:
    def __init__(self, zoom_type: str = "IN"):
        self.__start_lux_app()
        self.ws = create_connection("ws://localhost:3333/luxservice")
        self.set_liveview(True)
        self.set_zoom(zoom_type)

    def __start_lux_app(self):
        print("Start Lux Server")
        basefolder_loc = Path(__file__).parents[0]
        exe_loc = os.path.join(
            basefolder_loc, "LuxServer", "CytoSmartLuxService.exe"
        )
        subprocess.Popen(["cmd", "/K", exe_loc])

    def set_liveview(self, state: bool = True):
        msg1 = {"type": "LIVE_STREAM", "payload": {"enable": state}}
        self.ws.send(json.dumps(msg1))
        result = self.ws.recv()
        print(result)

    def set_zoom(self, zoom_type: str = "IN"):
        msg1 = {"type": "ZOOM", "payload": {"action": zoom_type.upper()}}
        self.ws.send(json.dumps(msg1))
        result = self.ws.recv()
        print(result)

    def get_image(self):
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
        result = self.ws.recv()
        print(result)
        
        count = 0
        while True:
            try:
                load_location = os.path.join(
                    r"C:\ProgramData", "CytoSmartLuxService", "Images", name
                )

                all_img_names = [i for i in os.listdir(load_location) if i.endswith(".jpg")]

                img = Image.open(os.path.join(load_location, max(all_img_names)))
                break
            except:
                count += 1
                print(f"failed {count} times to load image from experiment")
                time.sleep(1)
                if count >= 10:
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
    