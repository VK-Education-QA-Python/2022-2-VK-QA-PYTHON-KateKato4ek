import json
from flask import Flask, jsonify, request

USERS = {'Kateee': 1}

app = Flask(__name__)

@app.route('/vk_id/<username>', methods=['GET'])
def get_vk_id(username):
    if vk_id := USERS.get(username):
        return jsonify({'vk_id': vk_id}), 200
    else:
        return jsonify({}), 404

@app.route('/add', methods=['POST'])
def add_vk_id():
    username = json.loads(request.data)['username']
    vk_id = json.loads(request.data)['vk_id']
    if username not in USERS:
        USERS[username] = vk_id
        return jsonify({'vk_id': vk_id}), 201
    else:
        return jsonify(f'{username} already exists'), 400

app.run(host='0.0.0.0', port=8082)
