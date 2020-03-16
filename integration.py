#%%
import time

from luxconnector import LuxConnector

connector = LuxConnector()

s = time.time()
connector.get_image()
print(time.time() - s)