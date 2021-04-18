from urllib.parse import urlencode


class RestApi(object):
    API_URL = 'http://homster.pl/rest/'

    def __init__(self, endpoint=None):
        self.endpoint = None
        self.api_url = None
        self.set_end_point(endpoint)
        self.set_api_url(self.API_URL)

    def set_end_point(self, endpoint=None):
        if endpoint:
            endpoint_arr = str(endpoint).split('/')
            if len(endpoint_arr):
                self.endpoint = '/'.join(endpoint_arr) + '/'
            else:
                self.endpoint = None
        else:
            self.endpoint = None

    def set_api_url(self, url=None):
        if url is None:
            self.api_url = self.API_URL
        else:
            url_arr = str(url).split('/')
            if len(url_arr) > 1:
                if str(url_arr[0]).lower() == 'http:' or str(url_arr[0]).lower() == 'https:':
                    if str(url_arr[0]).lower() == 'http:':
                        ht = 'http://'
                    else:
                        ht = 'https://'
                    for n, val in enumerate(url_arr):
                        if str(val) == '':
                            url_arr.pop(n)
                    url_arr.pop(0)

                    self.api_url = ht + '/'.join(url_arr) + '/'
                else:
                    self.api_url = None
            else:
                self.api_url = None
