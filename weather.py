from restAPI import RestApi


class Weather(object):
    def __init__(self):
        self.chk_sns = 0
        self.sv_sns = 0

    def get_cfg(self):
        api = RestApi()
        rest = api.get_data('cfg/weather/')
        if rest['status'] == 200:
            commands = rest['data']['results']
            for com in commands:
                print(f'command:{com["name"]}={com["value"]}')


if __name__ == '__main__':
    weat = Weather()
    weat.get_cfg()
