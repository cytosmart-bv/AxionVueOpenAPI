#%%
import os
import time

from AxionVueOpenAPI import AxionVueOpenAPI

result_folder = os.path.join("results", "z_stack")
os.makedirs(result_folder, exist_ok=True)

connector = AxionVueOpenAPI(warranty=False)

serial_numbers = connector.get_all_serial_numbers()

if len(serial_numbers) > 0:
    s = time.time()
    z_stack = connector.get_z_stack(serial_numbers[0], 10, 0, 1)
    print(time.time() - s)
else:
    print("No devices are connected")

for idx, img in enumerate(z_stack):
    if img is None:
        print(f"idx {idx} is not found")
        continue
    img.save(os.path.join(result_folder, f"{idx}.png"), "JPEG")
