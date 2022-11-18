from urllib.parse import urljoin

import requests
import json
import os.path

from api.logger import Logger
from api.utils import random_string

class ResponseStatusCodeException(Exception):
    pass

class RespondErrorException(Exception):
    pass

class ApiClient:
    def __init__(self, base_url, login, password, repo_root):
        self.base_url = base_url
        self.login = login
        self.password = password
        self.repo_root = repo_root
    
        self.csrf_tocken = None
        self.session = requests.Session()
        self.logger = Logger()
        
        self.post_login()
    
    def get_csrf(self):
        resp = self._request(method='GET',
                             url=self.base_url,
                             location="csrf",
                             jsonify=False,
                             allow_redirects=True)
        return resp.cookies.get('csrftoken')
    
    def headers_csrf(self):
        return {'X-CSRFToken': self.csrf_tocken}
    
    def post_login(self):
        data = {
            "email": self.login,
            "password": self.password,
            'continue': f'{self.base_url}auth/mycom?state=target_login%3D1%26ignore_opener%3D1#email',
            'failure': 'https://account.my.com/login/'
        }
        headers = {
            'Referer': self.base_url
        }
        
        response = self._request(url='https://auth-ac.my.com',
                                 location="auth",
                                 method='POST',
                                 data=data,
                                 headers=headers,
                                 allow_redirects=True,
                                 jsonify=False)
        
        self.csrf_tocken = self.get_csrf()

        return response
    
    def get_source(self, source_link):
        params = {
            "_q": source_link
        }
        
        response = self._request(url=self.base_url,
                                 method='GET',
                                 location='api/v2/vk_groups.json',
                                 params=params)
        
        group_id = response["items"][0]["id"]
        
        self.logger.logger.info(f"GROUP_ID {group_id}")
        
        return group_id
    
    def post_source(self, group_id):
        json = {
            "items": [{"object_id": group_id}]
        }

        response = self._request(url=self.base_url,
                                 method='POST',
                                 location='api/v2/remarketing/vk_groups/bulk.json',
                                 json=json,
                                 headers=self.headers_csrf(),
                                 expected_status=201)

        source_id = response["items"][0]["id"]
        self.logger.logger.info(f"SOURCE_ID {id}")
    
        return source_id
    
    def post_segment_with_source(self, source_id):
        with open(os.path.join(self.repo_root, 'api/jsons/add_segment_with_group.json'), 'r') as f:
            segment_json = json.load(f)
        
        segment_json["relations"][0]["params"]["source_id"] = source_id
        
        segment_name = random_string()
        segment_json['name'] = segment_name
        
        self.logger.logger.info(f"SEGMENT_JSON {segment_json}")
        
        response = self._request(url=self.base_url,
                                 method='POST',
                                 location='api/v2/remarketing/segments.json',
                                 json=segment_json,
                                 headers=self.headers_csrf(),
                                 expected_status=200)
        
        segment_id = response["id"]
        self.logger.logger.info(f"SEGMENT_ID{segment_id}")
        
        return segment_id
    
    def check_segment_creation(self, segment_id):
        response = self._request(url=self.base_url,
                                location = (f"api/v2/remarketing/segments/{segment_id}/relations.json"),
                                method='GET',
                                jsonify=False)
        
        return response.ok
    
    def delete_segment(self, segment_id):
        json = [{
            "source_id": segment_id,
            "source_type": "segment"
        }]
        
        response = self._request(url=self.base_url,
                                 method='POST',
                                 location="api/v1/remarketing/mass_action/delete.json",
                                 headers=self.headers_csrf(),
                                 json=json,
                                 expected_status=200,
                                 jsonify=False)
        
        return response.ok
    
    def delete_source(self, source_id):
        response = self._request(url=self.base_url,
                                 method='DELETE',
                                 location=(f"api/v2/remarketing/vk_groups/{source_id}.json"),
                                 headers=self.headers_csrf(),
                                 expected_status=204,
                                 jsonify=False)
        
        return response.ok
    
    def post_segment(self):
        with open(os.path.join(self.repo_root, 'api/jsons/add_segment.json'), 'r') as f:
            segment_json = json.load(f)
            
        response = self._request(url=self.base_url,
                                 method='POST',
                                 location="api/v2/remarketing/segments.json",
                                 headers=self.headers_csrf(),
                                 json=segment_json,
                                 expected_status=200)
        segment_id = response["id"]
        self.logger.logger.info(f"SEGMENT_ID{segment_id}")
        
        return segment_id
    
    def _request(self,
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
        response = self.session.request(method=method,
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

    def post_image(self, image_path):
        files = {
            'file': open(image_path, 'rb'),
            'data': '{"width": 0, "height": 0,}'
        }
        response = self._request(url=self.base_url,
                                 method='POST',
                                 location='api/v2/content/static.json',
                                 expected_status=200,
                                 headers=self.headers_csrf(),
                                 files=files)
        image_id = response['id']
        
        return image_id
    
    def post_camp(self, image_id):
        with open(os.path.join(self.repo_root, 'api/jsons/add_campaign.json'), 'r') as f:
            campaign_json = json.load(f)
        
        campaign_json['banners'][0]['content']['image_240x400']['id'] = image_id
        
        campaign_name = random_string()
        campaign_json['name'] = campaign_name
        
        response = self._request(url=self.base_url,
                                 method='POST',
                                 location='api/v2/campaigns.json',
                                 expected_status=200,
                                 json=campaign_json,
                                 headers=self.headers_csrf())
        campaign_id = response["id"]
        
        return campaign_id
    
    def check_campaign_creation(self, campaign_id):
        params = {
            "_q": campaign_id
        }
        
        response = self._request(url=self.base_url,
                                 method='GET',
                                 location='api/v2/campaigns.json',
                                 expected_status=200,
                                 params=params)
        count = response["count"]
        
        return count == 1

    def delete_campaign(self, campaign_id):
        json = [{"id": campaign_id,
                 "status": "deleted"}]
        
        response = self._request(url=self.base_url,
                                 method='POST',
                                 location='api/v2/campaigns/mass_action.json',
                                 expected_status=204,
                                 headers=self.headers_csrf(),
                                 json=json,
                                 jsonify=False)
        
        return response.ok
        
        
        