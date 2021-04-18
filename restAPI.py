class RestApi(object):
    API_URL = 'http://homster.pl/rest/'

    def __init__(self, endpoint=None):
        self.endpoint = None
        self.api_url = None
        self.set_end_point(endpoint)

    def set_end_point(self, endpoint=None):
        if endpoint:
            endpoint_arr = str(endpoint).split('/')
            if len(endpoint_arr):
                self.endpoint = '/'.join(endpoint_arr) + '/'
            else:
                self.endpoint = None
        else:
            self.endpoint = None
