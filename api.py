from flask import Blueprint, request, jsonify, session, Response
from datetime import datetime
from funcs import *
from validation import *

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
        
        item_name = data.get('item_name')
        amount = data.get('amount')
        owned_by_username = data.get('owned_by')
        
        if not valid_item_name(item_name):
            return jsonify({'error': 'Invalid or missing item_name'}), 400
        
        if not valid_item_amount(amount):
            return jsonify({'error': 'Invalid or missing amount'}), 400
        
        if owned_by_username == 'null' or owned_by_username == 'Не привязано' or owned_by_username == '':
            owned_by_username = None # kostyl
        elif not user_exists(owned_by_username):
            return jsonify({'error':'User does not exist'}), 400

        error = add_item(item_name, amount, owned_by_username)
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
        owned_by_user = data.get('owned_by')

        if not valid_id(item_id):
            return jsonify({'error':'Invalid or missing item_id'}), 400
        
        if not item_exists(item_id):
            return jsonify({'error':'Item does not exist'}), 400

        if not valid_item_name(item_name):
            return jsonify({'error':'Invalid or missing item_name'}), 400
        
        if not valid_item_amount(amount):
            return jsonify({'error':'Invalid or missing amount'}), 400

        if not valid_item_condition(condition):
            return jsonify({'error':'Invalid or missing condition'}), 400

        if owned_by_user == 'null' or owned_by_user == '' or owned_by_user == 'Не привязано':
            owned_by_user = None #kostyl

        elif not valid_username(owned_by_user):
            return jsonify({'error':'Invalid or missing owned_by'}), 400
        
        elif not user_exists(owned_by_user):
            return jsonify({'error':'User does not exist'}), 400

        
        error = change_item(item_id, item_name, amount, condition, owned_by_user)
        if error:
            return jsonify({'error':'Unexpected error'}), 500
        return jsonify({'message':'Item changed successfully'}), 200

    return jsonify({'error':'No admin rights'}), 401


@api_blueprint.route('/deleteItem', methods=['POST'])
def delete_item_api():
    role = session.get('role')
    if role == 'admin':
        data = request.get_json()
        if not data:
            return jsonify({'error':'Invalid json provided'}), 400

        item_id = data.get('item_id')
        
        if not valid_id(item_id):
            return jsonify({'error':'Invalid or missing item_id'}), 400
        
        if not item_exists(item_id):
            return jsonify({'error':'Item does not exist'}), 400

        
        error = delete_item(item_id)
        if error:
            return jsonify({'error':'Unexpected error'}), 500
        return jsonify({'message':'Item deleted successfully'}), 200

    return jsonify({'error':'No admin rights'}), 401


@api_blueprint.route('/requestFix', methods=['POST'])
def request_fix_api():
    role = session.get('role')
    username = session.get('username')
    if role == 'admin' or role == 'user':
        data = request.get_json()
        user_id = get_id(username)
        if not data:
            return jsonify({'error':'Invalid json provided'}), 400

        item_id = data.get('item_id')
        
        if not valid_id(item_id):
            return jsonify({'error':'Invalid or missing item_id'}), 400
        if item_exists(item_id):
            if item_owned_by(item_id) == user_id:
                create_fix_request(item_id, user_id)
                return jsonify({'message':'Request created'}), 200
        return jsonify({'error':'Item does not exist or you are not the owner'}), 400
    return jsonify({'error':'Unauthorized'}), 401
        

@api_blueprint.route('/getFixRequests', methods=['GET'])
def get_fix_requests_api():
    role = session.get('role')
    if role == 'admin':
        requests = get_pending_fix_requests()
        return jsonify(requests), 200
    return jsonify({'error':'No admin rights'}), 401



@api_blueprint.route('/approveFixRequest', methods=['POST'])
def approve_fix_api():
    role = session.get('role')
    if role == 'admin':
        data = request.get_json()
        if not data:
            return jsonify({'error':'Invalid json provided'}), 400

        request_id = data.get('request_id')
        
        if not valid_id(request_id):
            return jsonify({'error':'Invalid or missing request_id'}), 400
        if is_fix_request_pending(request_id):
            approve_fix_request(request_id)
            return jsonify({'message':'Request approved'}), 200
        return jsonify({'error':'Request does not exist or already approved/denied'}), 400
    return jsonify({'error':'No admin rights'}), 401
 

@api_blueprint.route('/denyFixRequest', methods=['POST'])
def deny_fix_api():
    role = session.get('role')
    if role == 'admin':
        data = request.get_json()
        if not data:
            return jsonify({'error':'Invalid json provided'}), 400

        request_id = data.get('request_id')
        
        if not valid_id(request_id):
            return jsonify({'error':'Invalid or missing request_id'})
        if is_fix_request_pending(request_id):
            deny_fix_request(request_id)
            return jsonify({'message':'Request denied'}), 200
        return jsonify({'error':'Request does not exist or already approved/denied'}), 400
    return jsonify({'error':'No admin rights'}), 401
 

@api_blueprint.route('/requestInventory', methods=['POST'])
def request_inventory_api():
    role = session.get('role')
    username = session.get('username')
    if role == 'admin' or role == 'user':
        data = request.get_json()
        user_id = get_id(username)
        if not data:
            return jsonify({'error':'Invalid json provided'}), 400

        message = data.get('message')
        
        if not valid_message(message):
            return jsonify({'error':'Invalid or missing message'}), 400
        
        create_inventory_request(user_id, message)
        return jsonify({'message':'Request created'}), 200
    return jsonify({'error':'Unauthorized'}), 401
        

@api_blueprint.route('/getInventoryRequests', methods=['GET'])
def get_inventory_requests_api():
    role = session.get('role')
    if role == 'admin':
        requests = get_pending_inventory_requests()
        return jsonify(requests), 200
    return jsonify({'error':'No admin rights'}), 401



@api_blueprint.route('/approveInventoryRequest', methods=['POST'])
def approve_inventory_api():
    role = session.get('role')
    if role == 'admin':
        data = request.get_json()
        if not data:
            return jsonify({'error':'Invalid json provided'}), 400

        request_id = data.get('request_id')
        
        if not valid_id(request_id):
            return jsonify({'error':'Invalid or missing request_id'}), 400
        if is_inventory_request_pending(request_id):
            approve_inventory_request(request_id)
            return jsonify({'message':'Request approved'}), 200
        return jsonify({'error':'Request does not exist or already approved/denied'}), 400
    return jsonify({'error':'No admin rights'}), 401
 

@api_blueprint.route('/denyInventoryRequest', methods=['POST'])
def deny_inventory_api():
    role = session.get('role')
    if role == 'admin':
        data = request.get_json()
        if not data:
            return jsonify({'error':'Invalid json provided'}), 400

        request_id = data.get('request_id')
        
        if not valid_id(request_id):
            return jsonify({'error':'Invalid or missing request_id'})
            
        if is_inventory_request_pending(request_id):
            deny_inventory_request(request_id)
            return jsonify({'message':'Request denied'}), 200
        return jsonify({'error':'Request does not exist or already approved/denied'}), 400
    return jsonify({'error':'No admin rights'}), 401


@api_blueprint.route('/createOrder', methods=['POST'])
def create_order_api():
    role = session.get('role')
    if role == 'admin':
        data = request.get_json()
        if not data:
            return jsonify({'error':'Invalid json provided'}), 400
        
        item_name = data.get('item_name')
        amount = data.get('amount')
        price = data.get('price')
        supplier = data.get('supplier')

        if not valid_item_name(item_name):
            return jsonify({'error':'Invalid or missing item_name'}), 400
        if not valid_item_amount(amount):
            return jsonify({'error':'Invalid or missing amount'}), 400
        if not valid_item_price(price):
            return jsonify({'error':'Invalid or missing price'}), 400
        if not valid_supplier(supplier):
            return jsonify({'error':'Invalid or missing supplier'}), 400
        
        create_order(item_name, amount, price, supplier)
        return jsonify({'message':'Order created'}), 200
    return jsonify({'error':'No admin rights'}), 401


@api_blueprint.route('/changeOrder', methods=['POST'])
def change_order_api():
    role = session.get('role')
    if role == 'admin':
        data = request.get_json()
        if not data:
            return jsonify({'error':'Invalid json provided'}), 400
        
        order_id = data.get('id')
        item_name = data.get('item_name')
        amount = data.get('amount')
        price = data.get('price')
        supplier = data.get('supplier')

        if not valid_id(order_id):
            return jsonify({'error':'Invalid or missing id'}), 400
        if not valid_item_name(item_name):
            return jsonify({'error':'Invalid or missing item_name'}), 400
        if not valid_item_amount(amount):
            return jsonify({'error':'Invalid or missing amount'}), 400
        if not valid_item_price(price):
            return jsonify({'error':'Invalid or missing price'}), 400
        if not valid_supplier(supplier):
            return jsonify({'error':'Invalid or missing supplier'}), 400
        
        change_order(order_id, item_name, amount, price, supplier)
        return jsonify({'message':'Order changed'}), 200
    return jsonify({'error':'No admin rights'}), 401


@api_blueprint.route('/getOrders', methods=['GET'])
def get_orders_api():
    role = session.get('role')
    if role == 'admin':
        orders = get_orders()
        return jsonify(orders), 200
    return jsonify({'error':'No admin rights'}), 401


@api_blueprint.route('/generateReport', methods=['GET'])
def generate_report_api():
    role = session.get('role')
    if role == 'admin':
        data = get_all_items()
        output = create_excel(data)
        current_date = datetime.now().strftime("%Y-%m-%d")
        filename = f"report-{current_date}.xlsx"
        response = Response(
            output,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response.headers["Content-Disposition"] = f"attachment; filename={filename}"
        return response
    return jsonify({'error':'No admin rights'}), 401


@api_blueprint.route('/getMyInventoryRequests')
def get_my_inventory_requests_api():
    role = session.get('role')
    if role:
        username = session.get('username')
        uid = get_id(username)
        requests = get_user_inv_requests(uid)
        return jsonify(requests), 200
    return jsonify({'error':'Unauthorized'}), 401


@api_blueprint.route('/getMyFixRequests')
def get_my_fix_requests_api():
    role = session.get('role')
    if role:
        username = session.get('username')
        uid = get_id(username)
        requests = get_user_fix_requests(uid)
        return jsonify(requests), 200
    return jsonify({'error':'Unauthorized'}), 401


@api_blueprint.route('/autocomplete', methods=['POST'])
def autocomplete_api():
    role = session.get('role')
    if role == 'admin':
        
        data = request.get_json()

        if not data:
            return jsonify({'error':'Invalid json provided'}), 400
        
        usernameStart = data.get('user')

        if valid_username(usernameStart) or usernameStart == '':
            result = autocomplete(usernameStart)
            return jsonify(result)
        else:
            return jsonify({'error':'Invalid or missing user'}), 400

    return jsonify({'error':'No admin rights'}), 401