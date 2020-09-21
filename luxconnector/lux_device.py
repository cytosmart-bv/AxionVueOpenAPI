class LuxDevice:
    def __init__(self, serial_number, is_connected=True, temperature=None):
        self.serial_number = serial_number
        self.__temperature = temperature
        self.is_connected = is_connected

    @property
    def temperature(self):
        return self.__temperature

    @temperature.setter
    def temperature(self, new_temperature):
        self.__temperature = new_temperature

