from datetime import datetime

from max44009 import Max44009
from restAPI import RestApi
from sens_bme280 import Bme280Sensor


def check_type(val_in):
    try:
        val_i = int(val_in)
        if str(val_i) == str(val_in):
            return val_i
        else:
            return None
    except ValueError:
        pass

    if str(val_in) == 'None':
        return None
    if str(val_in) == 'True' or val_in == 'False':
        if val_in == 'True':
            return True
        else:
            return False

    if '.' in str(val_in):
        val_arr = str(val_in).split('.')
        if len(val_arr) == 2:
            try:
                val_i = float(val_in)
                if str(val_i) == val_in:
                    return val_i
            except ValueError:
                pass
    return val_in


class Weather(object):
    CFG_ENDPOINT = 'cfg/weather/'
    SV_ENDPOINT = 'weather/daily/'

    def __init__(self):
        self.chk_sns = None  # int [s]
        self.sv_sns = None  # int [min]
        self.week_sns = False  # boolean
        self.long_sns = False  # boolean
        self.new_sns_id = 0
        self.CFG_ENDPOINT = Weather.CFG_ENDPOINT
        self.SV_ENDPOINT = Weather.SV_ENDPOINT
        self.cfg_status = None
        self.bme = Bme280Sensor()
        self.max4 = Max44009()
        self.tms = datetime.now()
        self.rest_api = RestApi()
        self.measure = [
            0,  # num probe
            0,  # temperature
            0,  # pressure
            0,  # humidity
            0,  # luminance
        ]
        self.get_rest_cfg()
        if self.cfg_status == 200:
            print('Start modułu Pogody')
            self.cfg_status = True
            self.bmd = Bme280Sensor()
            self.max4 = Max44009()
        else:
            self.cfg_status = True
            print('Błąd połączenia przy pobieraniu konfiguracji modułu Pogody')

    def get_rest_cfg(self):
        api = RestApi()
        rest = api.get_data(self.CFG_ENDPOINT)
        print(f"api_url {api.get_rest_url()} status={rest['status']}")
        if rest['status'] == 200:
            self.cfg_status = rest['status']
            commands = rest['data']['results']
            for com in commands:
                self.__setattr__(com['name'], check_type(com["value"]))

    def get_measure(self):
        if self.cfg_status:
            self.measure = [x + y for x, y in zip(self.measure, self.bme.get_measure())]
            self.measure[4] += self.max4.get_luminance()
            print(
                f"n={self.measure[0]}, t={self.measure[1]}, p={self.measure[2]}, h={self.measure[3]}, l={self.measure[4]}")

    def save_measure(self):
        if self.cfg_status:
            time_probe = datetime.now()
            measure_data = {
                'time_m': f'{time_probe}',
                'temp_m': round(self.measure[1] / self.measure[0], 1),
                'pres_m': round(self.measure[2] / self.measure[0]),
                'humi_m': round(self.measure[3] / self.measure[0], 1),
                'ligh_m': round(self.measure[4] / self.measure[0]),
            }
            self.measure = [0 for _ in self.measure]
            rest = self.rest_api.send_data(self.SV_ENDPOINT, None, measure_data)
            # print(f'status={rest["status"]}')

    def event(self):
        if self.cfg_status:
            if self.chk_sns > 0:
                tms = datetime.now()
                if self.tms.second != tms.second:
                    if (self.chk_sns == 60 and tms.minute != self.tms.minute) or tms.second % self.chk_sns == 0:
                        print(f'-----> pomiar {tms}')
                        self.get_measure()
                    if self.sv_sns > 0:
                        if (self.chk_sns == 60 and tms.hour != self.tms.hour) or (
                                self.tms.minute != tms.minute and tms.minute % self.sv_sns == 0):
                            print(f'----------> zapis {tms}')
                            self.tms = tms
                            self.save_measure()
                            return True
                    self.tms = tms
        return False


if __name__ == '__main__':
    weat = Weather()
    weat.get_rest_cfg()
    i = 2
    while i:
        i -= 1
        print(f'--------- POMIAR {2 - i} ----------')
        n = 10
        while n:
            weat.get_measure()
            n -= 1
            sleep(1)
        weat.save_measure()
