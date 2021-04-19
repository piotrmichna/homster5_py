import json
from urllib.parse import urlencode

from urllib3 import PoolManager


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
                for n, v in enumerate(endpoint_arr):
                    if str(v) == '':
                        endpoint_arr.pop(n)
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
                    url_arr.pop(0)
                    for n, val in enumerate(url_arr):
                        if str(val) == '':
                            url_arr.pop(n)

                    self.api_url = ht + '/'.join(url_arr) + '/'
                else:
                    self.api_url = None
            else:
                self.api_url = None

    def get_rest_url(self, urldata=None):
        if self.api_url:
            if self.endpoint:
                url_rest = self.api_url + self.endpoint
            else:
                url_rest = self.api_url
            if type(urldata) is dict and len(urldata):
                return url_rest + '?' + urlencode(urldata)
            else:
                return url_rest
        else:
            return None

    def get_data(self, endpoint=None, url_data=None):
        self.set_end_point(endpoint)
        rest_url = self.get_rest_url(url_data)
        pm = PoolManager()
        rqst = pm.request('GET', rest_url)
        if rqst.status == 200:
            return {'status': rqst.status, 'data': json.load(rqst.data.decode('utf-8'))}
        else:
            return {'status': rqst.status}

    def send_data(self, endpoint=None, url_data=None, send_data=None, method='POST'):
        if type(send_data) is dict and len(send_data) and self.api_url:
            self.set_end_point(endpoint)
            rest_url = self.get_rest_url(url_data)
            encoded_data = json.dumps(send_data).encode('utf-8')
            pm = PoolManager()
            rqst = pm.request(method,
                              rest_url,
                              headers={'Content-Type': 'application/json'},
                              body=encoded_data)
            return {'status': rqst.status, 'data': json.load(rqst.data.decode('utf-8'))}
        else:
            return None
