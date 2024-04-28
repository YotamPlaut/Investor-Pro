from flask import Flask, jsonify, request
from backend.functions.user_database_manager import UserDatabaseManager
from backend.classes_backend.user import User

app = Flask(__name__)

@app.route('/alive', methods=['GET'])
def alive():
    return jsonify({'message':'alive'}), 200

@app.route('/create-new-account', methods=['POST'])
def create_new_account():

    print('in function')
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

if __name__ == '__main__':
    app.run(host='192.168.0.105', debug=True)