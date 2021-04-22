class SyncCommand(object):
    def __init__(self, endpoint: str, command: str, idc: int, value: str):
        self.command = command
        self.idc = idc
        self.value = value
        self.prefix = ""
        self.endpoint = endpoint
