#%%
import time

from luxconnector import LuxConnector

connector = LuxConnector()

serial_numbers = connector.get_all_serial_numbers()

if len(serial_numbers) > 0:
    s = time.time()
    img = connector.get_image(serial_numbers[0])
    print(time.time() - s)
else:
    print("No devices are connected")

s = time.time()
z_stack = connector.get_z_stack(serial_numbers[0], 10, 0, 1)
print(time.time() - s)