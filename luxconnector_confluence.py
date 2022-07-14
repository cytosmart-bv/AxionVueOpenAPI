#%%
import os

import cv2
import numpy as np

from luxconnector import LuxConnector
from confluency import Confluency

result_folder = os.path.join("results", "single_image")
os.makedirs(result_folder, exist_ok=True)

connector = LuxConnector(number_of_devices=1)

serial_number = connector.get_all_serial_numbers()[0]

connector.set_camera_settings(serial_number, "BRIGHTFIELD", 10)
connector.set_active_camera(serial_number, "BRIGHTFIELD")

img = connector.get_image(serial_number)
img_np = np.array(img)
if len(img_np.shape) > 2:
    img_np = img_np[:, :, 0]

cv2.imwrite(os.path.join(result_folder, f"raw_image.jpg"), img_np)

confluency = Confluency(2048)

multi_img, bin_img, confluency_percentage = confluency.calculate(img_np)

print(f"Confluency is {confluency_percentage:.2f}%")
cv2.imwrite(os.path.join(result_folder, f"results.jpg"), multi_img)
cv2.imwrite(os.path.join(result_folder, f"binary_results.jpg"), bin_img)