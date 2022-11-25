import json
from server_thread import ServerThread
from flask import Flask, jsonify, request

import settings

app = Flask(__name__)

SURNAME_DATA = {}

@app.route('/get_surname/<name>', methods=['GET'])
def get_user_surname(name):
    if surname := SURNAME_DATA.get(name):
        return jsonify(surname), 200
    
    else:
        return jsonify(f'Surname for user "{name}" not found'), 404
  
@app.route('/change_surname/<name>', methods=['PUT'])
def change_user_surname(name):
    if name in SURNAME_DATA:
        new_surname = json.loads(request.data)['surname']
        SURNAME_DATA['surname'] = new_surname
        data = {
            'name': name,
            'surname': new_surname
        }
        
        return jsonify(data), 200
    
    else:
        return jsonify(f'{name} does not exist'), 404

@app.route("/delete_surname/<name>", methods=["DELETE"])
def delete_user_surname(name):
    if name in SURNAME_DATA:
        SURNAME_DATA.pop(name)
        
        return jsonify({"status": "ok"}), 200
    
    else:
        return jsonify(f'User {name} not found and not deleted'), 404

def run():
    server = ServerThread(app, settings.MOCK_HOST, settings.MOCK_PORT)
    server.start()
    
    return server
