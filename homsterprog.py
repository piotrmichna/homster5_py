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

        # ---- set class property from rest data ----
        self.get_rest_cfg(data)

        if self.pin_cfg:
            self.SV_ENDPOINT = ProgGpio.SV_ENDPOINT + f'{self.pin_cfg}/'
            self.rest_api = RestApi()

        if ProgGpio.COUNTER == 0:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setwarnings(False)

        ProgGpio.COUNTER += 1

    def get_rest_cfg(self, data: dict):
        for key, val in data.items():
            if key == 'val':
                self.ob_state = val
            else:
                self.__setattr__(key, val)

        # GPIO Board pin initialization
        if self.dir_out:  # OUT
            GPIO.setup(self.pin_board, GPIO.OUT)
            if self.val_default:
                GPIO.output(self.pin_board, GPIO.LOW)
            else:
                GPIO.output(self.pin_board, GPIO.HIGH)

            if self.val == self.val_default:
                if self.val:
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
        print(f"rest_status={rest['status']}")

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

if __name__ == '__main__':
    pass
