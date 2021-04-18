class RestApi(object):
    API_URL = 'http://homster.pl/rest/'

    def __init__(self, endpoint=None):
        self.endpoint = None
        self.api_url = None
