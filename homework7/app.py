import json
from server_thread import ServerThread
from flask import Flask, request, jsonify

import settings

app = Flask(__name__)

app_data = {}
user_id_seq = 1

@app.route('/add_user', methods=['POST'])
def create_user():
    global user_id_seq
    
    user_name = json.loads(request.data)['name']
    if user_name not in app_data:
        app_data[user_name] = user_id_seq
        user_id_seq += 1
        return jsonify({'user_id': app_data[user_name]}), 201
    else:
        return jsonify(f'User_name {user_name} already exists: id: {app_data[user_name]}'), 400

@app.route('/get_user/<name>', methods=['GET'])
def get_user_id_by_name(name):
    if user_id := app_data.get(name):
        return jsonify({'user_id': user_id}), 200
    else:
        return jsonify(f'Username {name} not found'), 404

def run():
    server = ServerThread(app, settings.APP_HOST, settings.APP_PORT)
    server.start()
    
    return server
