class AxionVueDevice:
    def __init__(self, serial_number, is_connected=True, temperature=None):
        self.serial_number = serial_number
        self.__temperature = temperature
        self.is_connected = is_connected
        self.live_stream: bool = False
        self.x: float = -1.0
        self.y: float = -1.0
        self.is_sleeping: bool = True
        self.is_moving: bool = False
        self.is_auto_focusing: bool = False
        self.active_channel: str = "BRIGHTFIELD"

    @property
    def temperature(self):
        return self.__temperature

    @temperature.setter
    def temperature(self, new_temperature):
        self.__temperature = new_temperature

    @property
    def live_stream(self):
        return self.__live_stream

    @live_stream.setter
    def live_stream(self, new_live_stream: bool):
        self.__live_stream = new_live_stream
