#%%
import os
import time

from luxconnector import LuxConnector

result_folder = os.path.join("results", "single_image")
os.makedirs(result_folder, exist_ok=True)

connector = LuxConnector(number_of_devices=1)

serial_number = connector.get_all_serial_numbers()[0]

# BRIGHTFIELD
s = time.time()
connector.set_camera_settings(serial_number, "BRIGHTFIELD", 10)
connector.set_active_camera(serial_number, "BRIGHTFIELD")
img = connector.get_image(serial_number)
print(f"total time {time.time() - s}")
temperature = connector.get_temperature(serial_number)
print(f"temperature of {serial_number} is {temperature}")
img.save(os.path.join(result_folder, f"{serial_number}_BRIGHTFIELD_1.jpg"), "JPEG")

# RED
s = time.time()
connector.set_camera_settings(serial_number, "RED", 500)
connector.set_active_camera(serial_number, "RED")
img = connector.get_image(serial_number)
print(f"total time {time.time() - s}")
temperature = connector.get_temperature(serial_number)
print(f"temperature of {serial_number} is {temperature}")
img.save(os.path.join(result_folder, f"{serial_number}_RED.jpg"), "JPEG")

# GREEN
s = time.time()
connector.set_camera_settings(serial_number, "GREEN", 500)
connector.set_active_camera(serial_number, "GREEN")
img = connector.get_image(serial_number)
print(f"total time {time.time() - s}")
temperature = connector.get_temperature(serial_number)
print(f"temperature of {serial_number} is {temperature}")
img.save(os.path.join(result_folder, f"{serial_number}_GREEN.jpg"), "JPEG")