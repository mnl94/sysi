from flask import Blueprint, request, jsonify, session
from funcs import valid_username, valid_password, user_exists, register, get_role, correct_pw, get_owned_items, get_all_items, add_item

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/login', methods=['POST'])
def login_api():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if valid_username(username) and valid_password(password):
        if user_exists(username):
            if correct_pw(username,password):
                role = get_role(username)
                session['username'] = username
                session['role'] = role
                return jsonify({'message': 'Login successful'}), 200
    return jsonify({'error': 'Login Failed'}), 401


@api_blueprint.route('/register', methods=['POST'])
def register_api():
    error = None
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not valid_username(username):
        return jsonify({'error': 'Invalid username'}), 400

    if not valid_password(password):
        return jsonify({'error': 'Invalid password'}), 400

    if user_exists(username):
        return jsonify({'error': 'User already exists'}), 409

    code = register(username, password)
    if code == 0: return jsonify({'message': 'Registration successful'}), 201
    return jsonify({'error': 'Unexpected error'}), 500


@api_blueprint.route('/logout', methods=['GET'])
def logout_api():
    session.pop('username', None)
    session.pop('role', None)
    return jsonify({'message': 'Logged out successfully'}), 200


@api_blueprint.route('/getInventoryUser', methods=['GET'])
def inventory_api_user():
    username = session.get('username')
    role = session.get('role')
    if role == 'user':
        items = get_owned_items(username)
        return jsonify(items), 200
    return jsonify({'error':'Unauthorized'}), 401


@api_blueprint.route('/getInventoryAdmin', methods=['GET'])
def inventory_api_admin():
    role = session.get('role')
    if role == 'admin':
        items = get_all_items()
        return jsonify(items), 200
    return jsonify({'error':'No admin permissions'}), 401


@api_blueprint.route('/addItem', methods=['POST'])
def add_item_api():
    role = session.get('role')
    if role == 'admin':
        data = request.get_json()
        name = data.get('name')
        amount = data.get('amount')
        error = add_item(name, amount)
        if error == 0:
            return jsonify({'message':'Item added successfully!'}), 200
        return jsonify({'error':'Unexpected error'}), 500
    return jsonify({'error':'No admin permissions'}), 401
