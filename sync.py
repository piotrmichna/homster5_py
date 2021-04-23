from time import sleep

from restAPI import RestApi


class SyncCommand(object):
    ENDPOINT = 'sync/'

    def __init__(self, idc, command, value=None, endpoint=None):
        self.command = command
        if type(idc) == int:
            self.idc = idc
        else:
            self.idc = 0
        self.value = ""
        self.prefix = ""
        self.endpoint = ""
        if endpoint:
            self.parse_endpoint(endpoint)
        else:
            self.parse_endpoint(SyncCommand.ENDPOINT)

        self.set_value(value)
        self.set_prefix()

    def set_prefix(self):
        if type(self.command) == str and len(self.command):
            com_ar = self.command.split('_')
            while "" in com_ar:
                for i, s in enumerate(com_ar):
                    if s == "":
                        com_ar.pop(i)
            if len(com_ar) > 1:
                self.prefix = com_ar[0]
            else:
                self.prefix = ""
        else:
            self.prefix = ""

    def check_prefix(self, prefix):
        if self.prefix == prefix:
            return True
        else:
            if self.prefix == '' and not prefix:
                return True
            else:
                return False

    def parse_endpoint(self, endpoint):
        self.endpoint = ''
        if endpoint and self.idc and type(self.idc) == int:
            ep_ar = str(endpoint).split('/')
            while "" in ep_ar:
                for i, s in enumerate(ep_ar):
                    if s == "":
                        ep_ar.pop(i)
            if len(ep_ar):
                self.endpoint = '/'.join(ep_ar) + '/'
            if self.idc > 0:
                self.endpoint += str(self.idc) + '/'
            else:
                self.endpoint = ''

    def get_command_data(self, endpoint=None):
        if endpoint:
            self.parse_endpoint(endpoint)
        return {'endpoint': self.endpoint, 'data': {'value': self.value}}

    def set_value(self, value):
        if str(value).lower() == 'true' or str(value).lower() == 't' or (type(value) == int and value > 0):
            self.value = 'True'
        else:
            self.value = "False"

    def __str__(self):
        ret_str = f"<'endpoint':{self.endpoint}, 'command':{self.command}, "
        ret_str += f"'prefix':{self.prefix}, 'value': {self.value}>"
        return ret_str


class Sync(object):
    ENDPOINT = 'sync/'

    def __init__(self, endpoint=None):
        self.command_in = []
        self.command_out = []
        self.sync_delay = 1
        self.rest_api = RestApi()
        if endpoint:
            self.endpoint = str(endpoint)
        else:
            self.endpoint = Sync.ENDPOINT
        self.get_rest_status()
        self.check_status()

    def get_rest_status(self):
        rest = self.rest_api.get_data(self.endpoint)
        print(f"api_url={self.rest_api.get_rest_url()} status={rest['status']}")
        while True:
            if rest['status'] == 200:
                commands = rest['data']['results']
                tmp = []
                for com in commands:
                    tmp.append(SyncCommand(com['id'], com['name'], com['value']))
                    if len(self.command_out) < len(tmp):
                        self.command_out.append(SyncCommand(com['id'], com['name'], 'False'))

                self.command_in = tmp
                while len(self.command_out) > len(self.command_in):
                    self.command_out.pop(-1)
                break
            else:
                print("ERROR pobieranie stausu!!")
                print(f"api_url={self.rest_api.get_rest_url()} status={rest['status']}")
                sleep(0.1)

    def check_status(self):
        for idx in range(len(self.command_in)):
            print(f'command{self.command_in[idx].command}: in={self.command_in[idx].value} out=in={self.command_out[idx].value}')


if __name__ == '__main__':
    snc = Sync()
