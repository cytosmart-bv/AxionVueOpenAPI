#%%
import time

from luxconnector import LuxConnector

connector = LuxConnector()

# s = time.time()
# img = connector.get_image()
# print(time.time() - s)

s = time.time()
z_stack = connector.get_z_stack(10, 0, 1)
print(time.time() - s)