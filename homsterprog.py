import RPi.GPIO as GPIO


class ProgGpio(object):
    COUNTER = 0

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

        self.get_rest_cfg(data)
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
        else:  # IN
            if self.val_default:
                GPIO.setup(self.pin_board, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            else:
                GPIO.setup(self.pin_board, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def __del__(self):
        ProgGpio.COUNTER -= 1


if __name__ == '__main__':
    pass
