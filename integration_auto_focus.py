#%%
from AxionVueOpenAPI import AxionVueOpenAPI


connector = AxionVueOpenAPI(number_of_devices=1, warranty=False)

serial_number = connector.get_all_serial_numbers()[0]


connector.set_liveview(serial_number, True)
connector.open_liveview(
    serial_number,
)
connector.do_autofocus(serial_number, "CSslide")
