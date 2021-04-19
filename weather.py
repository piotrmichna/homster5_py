from restAPI import RestApi


def check_type(val_in):
    if val_in == 'None':
        return None
    if val_in == 'True' or val_in == 'False':
        if val_in == 'True':
            return True
        else:
            return False
    if val_in.isdigit():
        try:
            val_i = int(val_in)
            if str(val_i) == val_in:
                return val_i
            else:
                return None
        except ValueError:
            return None
    if '.' in val_in:
        val_arr = val_in.split('.')
        if len(val_arr) == 2:
            try:
                val_i = float(val_in)
                if str(val_i) == val_in:
                    return val_i
            except ValueError:
                pass
    return val_in


class Weather(object):
    def __init__(self):
        self.chk_sns = 0
        self.sv_sns = 0

    def get_cfg(self):
        api = RestApi()
        rest = api.get_data('cfg/weather/')
        print(f"odpowiedź {rest['status']}")
        print(f"api_url {api.get_rest_url()}")
        if rest['status'] == 200:
            commands = rest['data']['results']
            for com in commands:
                print(f'command:{com["name"]}={com["value"]}')


if __name__ == '__main__':
    weat = Weather()
    weat.get_cfg()
