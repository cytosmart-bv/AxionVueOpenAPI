#%%
import os

from CytoSmartOpenAPI import CytoSmartOpenAPI

result_folder = os.path.join("results", "single_image")
os.makedirs(result_folder, exist_ok=True)

connector = CytoSmartOpenAPI(number_of_devices=1, warranty=False)

serial_number = connector.get_all_serial_numbers()[0]

#%% set to 100, 100
print(connector.get_position(serial_number))

connector.move_stage(serial_number, 100, 100)
print(connector.get_position(serial_number))

#%% set to 0, 0
print(connector.get_position(serial_number))

connector.move_stage(serial_number, 18, 13)
print(connector.get_position(serial_number))

connector.set_focus(serial_number, 0.5)
connector.set_active_camera(serial_number, "BRIGHTFIELD")

img = connector.get_image(serial_number)
img.show()

#%% Test duration

connector.move_stage(serial_number, 18, 13)
connector.set_flash_duration(serial_number, 41)
img_dark = connector.get_image(serial_number)
img_dark.show()

connector.set_flash_duration(serial_number, 250)
img_light = connector.get_image(serial_number)
img_light.show()

#%% Change focus
connector.move_stage(serial_number, 18, 13)
connector.set_focus(serial_number, 0.1)

connector.set_focus(serial_number, 0.9)