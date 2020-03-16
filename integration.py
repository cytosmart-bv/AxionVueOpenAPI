#%%
import time

from luxconnector import LuxConnector

connector = LuxConnector()

s = time.time()
img = connector.get_image()
print(time.time() - s)