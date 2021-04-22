class SyncCommand(object):
    def __init__(self, endpoint: str, command: str, idc: int, value: str):
        self.command = command
        self.idc = idc
        self.value = value
        self.prefix = ""
        self.endpoint = endpoint
        self.set_prefix()

    def set_prefix(self):
        if type(self.command) == str and len(self.command):
            com_ar = self.command.split('_')
            if len(com_ar) > 1:
                self.prefix = com_ar[0]

    def check_prefix(self, prefix):
        if self.prefix == prefix:
            return True
        else:
            False
