from client import Client

from settings import APP_HOST, APP_PORT, MOCK_HOST, MOCK_PORT
from flask_mock import SURNAME_DATA

def test_add_user():
    client = Client(host=APP_HOST, port=APP_PORT)
    response = client.post(path='/add_user', json={'name': 'Kate'})
    assert 'user_id' in response
    
def test_get_user_surname():
     client = Client(host=MOCK_HOST, port=MOCK_PORT)
     SURNAME_DATA['Kate'] = 'Kachalova'
     surname = client.get(path='/get_surname/Kate')
     assert surname == 'Kachalova'
     SURNAME_DATA.clear()

def test_change_user_surname():
    client = Client(host=MOCK_HOST, port=MOCK_PORT)
    SURNAME_DATA['Kate'] = 'Kachalova'
    response = client.put(path='/change_surname/Kate', json={'surname': 'Katochek'})
    new_surname = response['surname']
    assert new_surname == 'Katochek'
    SURNAME_DATA.clear()
    
def test_delete_user_surname():
    client = Client(host=MOCK_HOST, port=MOCK_PORT)
    SURNAME_DATA['Kate'] = 'Kachalova'
    client.delete(path='/delete_surname/Kate')
    assert 'Kate' not in SURNAME_DATA
    SURNAME_DATA.clear()
