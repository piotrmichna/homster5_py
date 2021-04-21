import RPi.GPIO as GPIO

from restAPI import RestApi


class ProgGpio(object):
    COUNTER = 0
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
            if self.val_default:
                GPIO.output(self.pin_board, GPIO.LOW)
            else:
                GPIO.output(self.pin_board, GPIO.HIGH)
            if self.val == self.val_default:
                if self.val == 1:
                    self.send_rest_gpio(0)
                    self.val = 0
                else:
                    self.send_rest_gpio(1)
                    self.val = 1
        else:  # IN
            if self.val_default:
                GPIO.setup(self.pin_board, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            else:
                GPIO.setup(self.pin_board, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def send_rest_gpio(self, val):
        rest = self.rest_api.send_data(self.SV_ENDPOINT, None, {'val': val}, 'PATCH')

    def __del__(self):
        ProgGpio.COUNTER -= 1


class ProgStartTime(object):
    def __init__(self, data: dict):
        self.id = None
        self.name = None
        self.description = None
        self.day_delay = None
        self.start_time = None
        self.active = None
        self.prog = None
        self.get_rest_cfg(data)

    def get_rest_cfg(self, data: dict):
        for key, val in data.items():
            self.__setattr__(key, val)


class ProgX(object):
    def __init__(self, data: dict):
        self.id = None
        self.name = None
        self.active = None
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
    rest = ra.get_data('cfg/prog_name/')
    print(f'data.status={rest["status"]}')
    commands = rest['data']['results']
    prog = []
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
    prog[0].gpio_modules.pop(5)
    print('usuniecie gpio[5]')
    print(f'liczba gpio={ProgGpio.COUNTER}')
