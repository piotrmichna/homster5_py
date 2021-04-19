from datetime import datetime

from max44009 import Max44009
from restAPI import RestApi
from sens_bme280 import Bme280Sensor


def check_type(val_in):
    if str(val_in) == 'None':
        return None
    if val_in == 'True' or val_in == 'False':
        if val_in == 'True':
            return True
        else:
            return False
    if val_in.isdigit():
        try:
            val_i = int(val_in)
            if str(val_i) == val_in:
                return val_i
            else:
                return None
        except ValueError:
            return None
    if '.' in val_in:
        val_arr = val_in.split('.')
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
        self.CFG_ENDPOINT = Weather.CFG_ENDPOINT
        self.SV_ENDPOINT = Weather.SV_ENDPOINT
        self.cfg_status = None
        self.bme = Bme280Sensor()
        self.max4 = Max44009()
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

    def save_measure(self):
        if self.cfg_status:
            self.measure[1] = round(self.measure[1] / self.measure[0], 1)
            self.measure[2] = round(self.measure[2] / self.measure[0])
            self.measure[3] = round(self.measure[3] / self.measure[0], 1)
            self.measure[4] = round(self.measure[4] / self.measure[0])
            time_probe = datetime.now()
            time_probe.second = 0
            time_probe.microsecond = 0
            measure_data = {
                'time_m': f'{time_probe}',
                'temp_m': round(self.measure[1] / self.measure[0], 1),
                'pres_m': round(self.measure[2] / self.measure[0]),
                'humi_m': round(self.measure[3] / self.measure[0], 1),
                'ligh_m': round(self.measure[4] / self.measure[0]),
            }
            self.measure = [0 for _ in self.measure]
            api = RestApi()
            rest = api.send_data(self.SV_ENDPOINT, None, measure_data)


if __name__ == '__main__':
    weat = Weather()
    weat.get_rest_cfg()
