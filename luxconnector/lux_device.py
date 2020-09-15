class LuxDevice:
    def __init__(self, serial_number, is_connected=True, tempature=None):
        self.serial_number = serial_number
        self.__tempature = tempature
        self.is_connected = is_connected

    @property
    def tempature(self):
        return self.__tempature

    @tempature.setter
    def tempature(self, new_tempature):
        self.__tempature = new_tempature

