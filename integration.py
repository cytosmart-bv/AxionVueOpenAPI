#%%
import os
import time

from luxconnector import LuxConnector

result_folder = os.path.join("results", "single_image")
os.makedirs(result_folder, exist_ok=True)

connector = LuxConnector(number_of_devices=1)

serial_numbers = connector.get_all_serial_numbers()

for serial_number in serial_numbers:
    s = time.time()
    img = connector.get_image(serial_number)
    print(f"total time {time.time() - s}")
    temperature = connector.get_temperature(serial_number)
    print(f"temperature of {serial_number} is {temperature}")
    img.save(os.path.join(result_folder, f"{serial_number}_{int(time.time())}.png"), "JPEG")
