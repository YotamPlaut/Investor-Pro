import datetime

from flask import Flask, jsonify, request
from backend.functions.user_database_manager import UserDatabaseManager
from backend.functions.event_db_manager import EventDatabaseManager
from backend.classes_backend.user import User

app = Flask(__name__)


@app.route('/alive', methods=['GET'])
def alive():
    return jsonify({'message':'alive'}), 200


@app.route('/create-new-account', methods=['POST'])
def create_new_account():

    function_called_timestamp = datetime.datetime.now()
    # Get account details from the request
    data = request.json

    # Check if all required fields are provided
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    user_db_manager = UserDatabaseManager()

    # Check if the username is already taken
    if user_db_manager.is_username_exists(data['username']):
        return jsonify({'error': 'Username already taken'}), 400

    new_user = User(username=data['username'], password=data['password'], email=data['email'])
    user_db_manager.load_new_user_to_database(new_user)

    event_db_manager = EventDatabaseManager()
    event_db_manager.insert_raw_action('sign_up', function_called_timestamp, data['username'])

    return jsonify({'message': 'Account added successfully'}), 201


@app.route('/get-all-users-info', methods=['GET'])
def get_all_users_info():
    user_db_manager = UserDatabaseManager()
    data = user_db_manager.get_all_users_info()
    print(data)
    print(type(data))
    return jsonify({'message': 'test'}), 200


@app.route('/get-all-events', methods=['GET'])
def get_all_events():
    events_db_manager = EventDatabaseManager()
    data = events_db_manager.get_all_events()
    print(data)
    print(type(data))
    return jsonify({'message': 'test'}), 200


@app.route('/change-password', methods=['POST'])
def change_password():

    curr_datetime = datetime.datetime.now()
    data = request.json
    if 'username' not in data or 'new_password' not in data or 'old_password' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    user_db_manager = UserDatabaseManager()

    # Check if the username exists in db
    if not user_db_manager.is_username_exists(data['username']):
        return jsonify({'error': 'Invalid Username'}), 400

    if user_db_manager.authenticate_user_password(data['username'], data['old_password']):
        user_db_manager.change_password(data['username'], data['new_password'])
        event_db_manager = EventDatabaseManager()
        event_db_manager.insert_raw_action('password_change', curr_datetime, data['username'])
        return jsonify({'message': 'successfully changed password'}), 200
    else:
        return jsonify({'error': 'incorrect password'}), 404


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if 'username' not in data or 'password' not in data :
        return jsonify({'error': 'Missing required fields'}), 400
    else:
        db_manager = UserDatabaseManager()
        if (db_manager.authenticate_user_password()):
            return jsonify({'message': 'successfully logged in'}), 200
        else:
            return jsonify({'error': 'invalid username or password'}), 404


@app.route('/create_new_protfolio', methods=['POST'])
def create_new_protfolio():
    data = request.json
    if 'username' not in data or 'protfolio_id' not in data or 'stocks_id' not in data:
        return jsonify({'error': 'Missing required fields'}), 400




if __name__ == '__main__':
    # app.run(debug=True)
    # to allow machines in my network access the server
    # run the following function with the none local host ip it prints on the screen
    app.run(host='0.0.0.0', port=5000, debug=True)
