import bme280
import smbus2


class Bme280Sensor(object):
    PORT = 1
    ADDRESS = 0x76

    def __init__(self, adr=None, port=None):
        if adr is not None and '0x' in adr:
            self.ADDRESS = adr
        else:
            self.ADDRESS = Bme280Sensor.ADDRESS
        if port is not None and type(port) is int:
            self.PORT = port
        else:
            self.PORT = Bme280Sensor.PORT
        self.buss = smbus2.SMBus(self.PORT)
        self.calibration_params = bme280.load_calibration_params(self.buss, self.ADDRESS)
        self.data = None

    def get_measure(self):
        self.data = bme280.sample(self.buss, self.ADDRESS, self.calibration_params)
        self.data.pressure = self.data.pressure + 9
        return [1, round(self.data.temperature, 2), round(self.data.pressure, 1),
                round(self.data.humidity), 0]

    def get_print(self):
        print(f"    data pomiaru: {self.data.timestamp}")
        print(f'     temperatura: {round(self.data.temperature, 2)}')
        print(f'       ciśnienie: {round(self.data.pressure)},1')
        print(f"      wilgotność: {round(self.data.humidity, 1)}")


if __name__ == '__main__':
    be = Bme280Sensor()
    be.get_measure()
    be.get_print()
