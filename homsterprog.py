from datetime import datetime
from time import sleep

import RPi.GPIO as GPIO

from restAPI import RestApi


class ProgGpio(object):
    COUNTER = 0
    GPIO_UPDATE = True
    SV_ENDPOINT = 'cfg/gpio_pin/'

    def __init__(self, data: dict):
        # ------- property hardware ----------
        self.id = None  # id module
        self.prog = None  # id module
        self.lp = None  # ordering
        self.duration_sec = None  # time tu run
        self.enabled = True  # is enabled pin
        self.pin_cfg = None  # id row in GpioPinCfg
        self.name = None  # name of device
        self.pin_board = None  # nr pin IO on raspberry pi board
        self.dir_out = None  # pin out
        self.val = None  # actual pin IO state
        self.val_set = None
        self.val_default = None  # active pin IO state

        # ------- property object ----------
        self.ob_duration_elspet = 0
        self.ob_state = None
        self._started = False
        self.rest_api = RestApi()
        if ProgGpio.COUNTER == 0:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setwarnings(False)

        ProgGpio.COUNTER += 1

        # ---- set class property from rest data ----
        self.get_rest_cfg(data)

    def get_rest_cfg(self, data: dict):
        for key, val in data.items():
            self.__setattr__(key, val)

        # GPIO Board pin initialization
        if self.pin_cfg:
            self.SV_ENDPOINT = ProgGpio.SV_ENDPOINT + f'{self.pin_cfg}/'

        if self.dir_out:  # OUT
            GPIO.setup(self.pin_board, GPIO.OUT)
            self.set_gpio_off()
        else:  # IN
            if self.val_default:
                GPIO.setup(self.pin_board, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            else:
                GPIO.setup(self.pin_board, GPIO.IN, pull_up_down=GPIO.PUD_UP)

            if self.val != GPIO.input(self.pin_board):
                rest = self.send_rest_gpio(GPIO.input(self.pin_board))
                ProgGpio.GPIO_UPDATE = True

    def send_rest_gpio(self, val):
        print(f'rest_gpio[{self.pin_board}]={val}')
        rest = self.rest_api.send_data(self.SV_ENDPOINT, None, {'val': val}, 'PATCH')
        return rest['status']

    def set_gpio_on(self):
        if self.enabled:
            if GPIO.input(self.pin_board) != self.val_default:
                GPIO.output(self.pin_board, self.val_default)
            if self.val != self.val_default:
                rest = self.send_rest_gpio(self.val_default)
                ProgGpio.GPIO_UPDATE = True

    def set_gpio_off(self):
        if GPIO.input(self.pin_board) == self.val_default:
            GPIO.output(self.pin_board, int(not bool(self.val_default)))

        if self.val == self.val_default:
            rest = self.send_rest_gpio(int(not bool(self.val_default)))
            ProgGpio.GPIO_UPDATE = True

    def __del__(self):
        ProgGpio.COUNTER -= 1


class ProgStartTime(object):
    ENDPOINT = 'cfg/prog_start/'
    UPDATE = True

    def __init__(self, data: dict):
        self.id = None
        self.name = None
        self.description = None
        self.day_delay = None
        self.next_time = None
        self.start_time = None
        self.active = None
        self.prog = None
        self.rest_api = RestApi()
        self.SV_ENDPOINT = None
        self.get_rest_cfg(data)

    def get_rest_cfg(self, data: dict):
        for key, val in data.items():
            if key == 'next_time':
                self.next_time = datetime.fromisoformat(val)
            else:
                self.__setattr__(key, val)
        print(f'start[{self.name}]={self.start_time}')
        self.SV_ENDPOINT = ProgStartTime.ENDPOINT + str(self.id) + '/'
        self.get_start_time()

    def check_next_start(self, dat):
        if self.next_time < dat:
            return self.next_time
        else:
            return dat

    def get_start_time(self):
        if self.active:
            now = datetime.now()
            now = now.replace(microsecond=0)
            # print(
            #     f'dziśiejszy start ={bool(now.timetuple().tm_yday <= self.next_start.timetuple().tm_yday)}')

            tim_ar = str(self.start_time).split(':')
            start_t = now.replace(hour=int(tim_ar[0]), minute=int(tim_ar[1]), second=int(tim_ar[2]), microsecond=0)
            # start_t5 = now.replace(hour=int(tim_ar[0]), minute=int(tim_ar[1]), second=int(tim_ar[2]) + 5,
            #                        microsecond=0)
            # if (now >= start_t) and (now <= start_t5):
            #     print(f'Pora na start: {self.name}')
            # elif now < start_t:
            #     print(f'....Oczekiwanie na start: {self.name}')
            # else:
            #     print(f'....Za późno na start: {self.name}')
            # print(f'{start_t.isoformat()}={self.next_time}')
            if start_t != self.next_time:
                while True:
                    rest = self.rest_set_next_start(start_t)
                    if rest['status'] == 200:
                        self.next_time = start_t
                        break
                    else:
                        sleep(0.1)

            # elsped = start_t - now
            # print(f'start_za={elsped}')
            # print(f'dzień_roku={now.timetuple().tm_yday}')

    def rest_set_next_start(self, val):
        print(f'rest_next_start[{self.name}]={val}')
        rest = self.rest_api.send_data(self.SV_ENDPOINT, None, {'next_time': str(val)}, 'PATCH')
        print(f"rest status ---> {rest['status']}")
        return rest


class ProgX(object):
    def __init__(self, data: dict):
        self.id = None
        self.name = None
        self.active = None
        self.running = None
        self.stop_run = False
        self.start_times = []
        self.gpio_modules = []
        self.get_rest_cfg(data)

    def get_rest_cfg(self, data: dict):
        for key, val in data.items():
            if key == 'progpin':
                for mod in val:
                    self.gpio_modules.append(ProgGpio(mod))
            elif key == 'progstarts':
                for mod in val:
                    self.start_times.append(ProgStartTime(mod))
            else:
                self.__setattr__(key, val)

    def __str__(self):
        return f'{self.name}, start_times({len(self.start_times)}), gpio_module({len(self.gpio_modules)})'


if __name__ == '__main__':
    ra = RestApi()
    ProgGpio.GPIO_UPDATE = True
    while ProgGpio.GPIO_UPDATE:
        prog = []
        ProgGpio.GPIO_UPDATE = False
        rest = ra.get_data('cfg/prog_name/')
        print(f'----> data.status={rest["status"]}')
        commands = rest['data']['results']

        mods = rest['data']['results']
        for mod in mods:
            prog.append(ProgX(mod))

        print(f'ilosc programow={len(prog)}')
    for n, pr in enumerate(prog):
        print(f'program{n}={pr.name}')
        if pr.id:
            print(f'ilość startów programu={len(pr.start_times)}')
            for st in pr.start_times:
                print(f'---> name={st.name}, start={st.start_time}')
            print(f'ilość gpio programu={len(pr.gpio_modules)}')
            for mod in pr.gpio_modules:
                print(f'---> gpio={mod.name}, start={mod.pin_board}')
            print(pr)
    print(f'liczba gpio={ProgGpio.COUNTER}')

    print(f'liczba gpio={ProgGpio.COUNTER}')
