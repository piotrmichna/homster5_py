class SyncCommand(object):
    def __init__(self, endpoint: str, command: str, idc: int, value: str):
        self.command = command
        self.idc = idc
        self.value = ""
        self.prefix = ""
        self.endpoint = ""
        self.set_value(value)
        self.set_prefix()
        self.parse_endpoint(endpoint)

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

    def parse_endpoint(self, endpoint: str):
        ep_ar = endpoint.split('/')
        for i, s in enumerate(ep_ar):
            if s == "":
                ep_ar.pop(i)
        if len(ep_ar):
            self.endpoint = '/'.join(ep_ar) + '/' + self.idc + '/'
        else:
            self.endpoint = self.idc + '/'

    def get_command_data(self, endpoint=None):
        if endpoint:
            self.parse_endpoint(endpoint)
        return {'endpoint': self.endpoint, 'data': {'value': self.value}}

    def set_value(self, value):
        if value:
            self.value = str(value)
        else:
            self.value = ""

    def __str__(self):
        ret_str = f"<'endpoint':{self.endpoint}, 'command':{self.command}, "
        ret_str += f"'prefix':{self.prefix}, 'value': {self.value}>"
        return ret_str
