from flask import Blueprint, request, jsonify, session
from funcs import user_exists, register, get_role, correct_pw, get_owned_items, get_all_items, add_item, change_item
from validation import valid_username, valid_password, valid_role, valid_item_name, valid_item_amount, valid_item_condition

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
    if role == 'user' or role == 'admin':
        items = get_owned_items(username)
        return jsonify(items), 200
    return jsonify({'error':'Unauthorized'}), 401


@api_blueprint.route('/getInventoryAdmin', methods=['GET'])
def inventory_api_admin():
    role = session.get('role')
    if role == 'admin':
        items = get_all_items()
        return jsonify(items), 200
    return jsonify({'error':'No admin rights'}), 401


@api_blueprint.route('/addItem', methods=['POST'])
def add_item_api():
    role = session.get('role')
    if role == 'admin':
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid json provided'}), 400
        
        name = data.get('name')
        amount = data.get('amount')
        
        if not valid_item_name(name):
            return jsonify({'error': 'Invalid or missing name'}), 400
        
        if not valid_item_amount(amount):
            return jsonify({'error': 'Invalid or missing amount'}), 400

        error = add_item(name, amount)
        if error == 0:
            return jsonify({'message':'Item added successfully!'}), 200
        
        return jsonify({'error':'Unexpected error'}), 500
    return jsonify({'error':'No admin rights'}), 401


@api_blueprint.route('/changeItem', methods=['POST'])
def change_item_api():
    role = session.get('role')
    if role == 'admin':
        data = request.get_json()
        if not data:
            return jsonify({'error':'Invalid json provided'}), 400

        item_id = data.get('item_id')
        item_name = data.get('item_name')
        amount = data.get('amount')
        condition = data.get('condition')
        owned_by_user = data.get('owned_by_user')

        if not valid_item_name(item_name):
            return jsonify({'error':'Invalid or missing item_name'}), 400
        
        if not valid_item_amount(amount):
            return jsonify({'error':'Invalid or missing amount'}), 400

        if not valid_item_condition(condition):
            return jsonify({'error':'Invalid or missing condition'}), 400

        if not valid_username(owned_by_user):
            return jsonify({'error':'Invalid or missing owned_by_user'}), 400

        if not user_exists(owned_by_user):
            return jsonify({'error':'User does not exist'}), 400

        
        error = change_item(item_id, item_name, amount, condition, owned_by_user)
        if error:
            return jsonify({'error':'Unexpected error'}), 500
        return jsonify({'message':'Item changed successfully'}), 200

    return jsonify({'error':'No admin rights'}), 401
