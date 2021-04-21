class ProgGpio(object):
    def __init__(self):
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


if __name__ == '__main__':
    pass
