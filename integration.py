#%%
import os
import time

import cv2

from luxconnector import LuxConnector

result_folder = os.path.join("results", "single_image")
os.makedirs(result_folder, exist_ok=True)

connector = LuxConnector()

serial_numbers = connector.get_all_serial_numbers()

if len(serial_numbers) > 0:
    s = time.time()
    connector.set_focus(serial_numbers[0], 0)
    img = connector.get_image(serial_numbers[0])
    print(time.time() - s)
else:
    print("No devices are connected")

img.save(os.path.join(result_folder, f"{time.time()}.png"), "JPEG")
