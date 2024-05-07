from flask import Flask, jsonify, request
from backend.functions.user_database_manager import UserDatabaseManager
from backend.classes_backend.user import User

app = Flask(__name__)


@app.route('/alive', methods=['GET'])
def alive():
    return jsonify({'message':'alive'}), 200


@app.route('/create-new-account', methods=['POST'])
def create_new_account():

    # Get account details from the request
    data = request.json

    # Check if all required fields are provided
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    db_manager = UserDatabaseManager()

    # Check if the username is already taken
    if db_manager.is_username_exists(data['username']):
        return jsonify({'error': 'Username already taken'}), 400

    new_user = User(username=data['username'], password=data['password'], email=data['email'])
    db_manager.load_new_user_to_database(new_user)

    return jsonify({'message': 'Account added successfully'}), 201


@app.route('/get-all-users-info', methods=['GET'])
def get_all_users_info():
    db_manager = UserDatabaseManager()
    data = db_manager.get_all_users_info()
    print(data)
    print(type(data))
    return jsonify({'message': 'test'}), 200


@app.route('/change-password', methods=['POST'])
def change_password():

    data = request.json
    if 'username' not in data or 'new_password' not in data or 'old_password' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    db_manager = UserDatabaseManager()

    # Check if the username exists in db
    if not db_manager.is_username_exists(data['username']):
        return jsonify({'error': 'Invalid Username'}), 400

    if db_manager.authenticate_user_password(data['username'], data['old_password']):
        db_manager.change_password(data['username'], data['new_password'])
        return jsonify({'message': 'successfully changed password'}), 200
    else:
        return jsonify({'error': 'incorrect password'}), 404


if __name__ == '__main__':
    # app.run(debug=True)
    # to allow machines in my network access the server
    # run the following function with the none local host ip it prints on the screen
    app.run(host='0.0.0.0', port=5000, debug=True)
