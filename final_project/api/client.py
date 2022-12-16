import requests
import json
import os.path

from urllib.parse import urljoin
import allure

from utils.logger import Logger
from fixtures import *

class ResponseStatusCodeException(Exception):
    pass

class RespondErrorException(Exception):
    pass

class ApiClient:
    def __init__(self, base_url, username, password, repo_root):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.repo_root = repo_root
        
        self.logger = Logger()
        self.session_without_auth = self.session_without_auth()
        self.session_with_auth = self.session_with_auth()
    
    def session_without_auth(self):
        session = requests.Session()
        return session

    def session_with_auth(self):
        session = requests.Session()
        self.login(session, username=self.username, password=self.password)
        return session
    
    def _request(self,
                 session,
                 url,
                 method,
                 location,
                 data={},
                 json={},
                 headers={},
                 files={},
                 params=None,
                 allow_redirects=False,
                 expected_status=200,
                 jsonify=True):
        url = urljoin(url, location)

        self.logger.log_request(url, expected_status)
        response = session.request(method=method,
                                        url=url,
                                        headers=headers,
                                        data=data,
                                        params=params,
                                        json=json,
                                        files=files,
                                        allow_redirects=allow_redirects)
        self.logger.log_response(response)

        if response.status_code != expected_status:
            raise ResponseStatusCodeException(f'Expected {expected_status}, but got {response.status_code}')
        if jsonify:
            json_response: dict = response.json()
            if json_response.get('bStateError', False):
                error = json_response['sErrorMsg']
                raise RespondErrorException(f'Request {url} return error : "{error}"')

            return json_response
        return response
    
    @allure.step('Логин')
    def login(self, session, username, password, expected_status=200):
        data = {
            "username": username,
            "password": password,
            'submit': 'Login'
        }
        
        response = self._request(session,
                                 url=self.base_url,
                                 location='login',
                                 method='POST',
                                 data=data,
                                 allow_redirects=True,
                                 jsonify=False,
                                 expected_status=expected_status)

        return response
    
    @allure.step('Логаут')
    def logout(self, session):
        response = self._request(session,
                                 url=self.base_url,
                                 location='logout',
                                 method='GET',
                                 allow_redirects=True,
                                 jsonify=False,
                                 expected_status=200)

    @allure.step('Регистрация')
    def reg_user(self, session, name, surname, middlename, username, email, password, confirmpassword, expected_status):
        data = {
            "name": name,
            "surname": surname,
            "middlename": middlename,
            "username": username,
            "email": email,
            "password": password,
            "confirm": confirmpassword,
            "term": 'y',
            'submit': 'Register'
            }
        
        response = self._request(session,
                                 url=self.base_url,
                                 location='reg',
                                 method='POST',
                                 data=data,
                                 allow_redirects=True,
                                 jsonify=False,
                                 expected_status=expected_status)
        
        return response
