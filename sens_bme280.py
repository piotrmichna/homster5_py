import bme280
import smbus2


class Bme280Sensor(object):
    PORT = 1
    ADDRESS = 0x76

    def __init__(self, adr=None, port=None):
        if adr is not None:
            self.ADDRESS = 0x76
        if port is not None:
            self.PORT = port
        self.buss = smbus2.SMBus(self.PORT)
        self.calibration_params = bme280.load_calibration_params(self.buss, self.ADDRESS)
        self.data = None

    def get_measure(self):
        self.data = bme280.sample(self.buss, self.ADDRESS, self.calibration_params)
        return {
            'temp': round(self.data.temperature, 2),
            'humi': round(self.data.pressure, 1),
            'pres': round(self.data.humidity)
        }

    def get_print(self):
        print(f"    data pomiaru: {self.data.timestamp}")
        print(f'     temperatura: {round(self.data.temperature, 2)}')
        print(f'       ciśnienie: {round(self.data.pressure)}')
        print(f"      wilgotność: {round(self.data.humidity,1)}")


if __name__ == '__main__':
    be = Bme280Sensor()
    be.get_measure()
    be.get_print()
