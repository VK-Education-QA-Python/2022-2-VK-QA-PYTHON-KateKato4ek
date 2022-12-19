import requests
from urllib.parse import urljoin

from logger import Logger

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.session = requests.Session()
        self.logger = Logger()
    
    def get(self, path):
        response = self._request(method='GET', path=path)
        
        return response
    
    def post(self, path, json):
        response = self._request(method='POST', path=path, json=json)
        
        return response
    
    def put(self, path, json):
        response = self._request(method='PUT', path=path, json=json)
        
        return response
    
    def delete(self, path):
        response = self._request(method='DELETE', path=path)
        
        return response
        
        
    def _request(self,
                 method,
                 path,
                 data={},
                 json={},
                 headers={},
                 files={},
                 params=None):
        url = urljoin(f'http://{self.host}:{self.port}', path)

        self.logger.log_request(url)
        response = self.session.request(method=method,
                                        url=url,
                                        headers=headers,
                                        data=data,
                                        params=params,
                                        json=json,
                                        files=files,
                                        allow_redirects=True)
        self.logger.log_response(response)
        
        return response.json()
