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
