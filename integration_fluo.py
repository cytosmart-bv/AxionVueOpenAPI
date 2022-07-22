#%%
import os
import time

from CytoSmartOpenAPI import CytoSmartOpenAPI

result_folder = os.path.join("results", "single_image")
os.makedirs(result_folder, exist_ok=True)

connector = CytoSmartOpenAPI(number_of_devices=1)

serial_number = connector.get_all_serial_numbers()[0]

# BRIGHTFIELD
s = time.time()
connector.set_camera_settings(serial_number, "BRIGHTFIELD", 10)
connector.set_active_camera(serial_number, "BRIGHTFIELD")
img = connector.get_image(serial_number)
img.save(os.path.join(result_folder, f"{serial_number}_BRIGHTFIELD10_.jpg"), "JPEG")

# BRIGHTFIELD
s = time.time()
connector.set_camera_settings(serial_number, "BRIGHTFIELD", 5)
connector.set_active_camera(serial_number, "BRIGHTFIELD")
img = connector.get_image(serial_number)
img.save(os.path.join(result_folder, f"{serial_number}_BRIGHTFIELD5_.jpg"), "JPEG")

# RED
s = time.time()
connector.set_camera_settings(serial_number, "RED", 500, gain=30, brightness=5000)
connector.set_active_camera(serial_number, "RED")
img = connector.get_image(serial_number)
img.save(os.path.join(result_folder, f"{serial_number}_RED.jpg"), "JPEG")

# GREEN
s = time.time()
connector.set_camera_settings(serial_number, "GREEN", 500)
connector.set_active_camera(serial_number, "GREEN")
img = connector.get_image(serial_number)
img.save(os.path.join(result_folder, f"{serial_number}_GREEN.jpg"), "JPEG")

# GREEN z-stack
connector.set_active_camera(serial_number, "GREEN")
z_stack = connector.get_z_stack(serial_number, num_img=10 ,start_focus=0.1, stop_focus=0.2)

for idx, img in enumerate(z_stack):
    img.save(os.path.join(result_folder, f"{serial_number}_GREEN_z{str(idx).zfill(3)}.jpg"), "JPEG")

