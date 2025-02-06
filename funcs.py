import os
import bcrypt
from dotenv import load_dotenv
import mysql.connector
from openpyxl import Workbook
from io import BytesIO

load_dotenv()


MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')

# Подключение к базе данных
conn = mysql.connector.connect(
    host="localhost",
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE
)

curs = conn.cursor()

with open('schema.sql', 'r') as file:
    sql = file.read()

# читаем схему и создаём 
curs.execute(sql, multi=True)
curs.close()

#почему-то после того как я запускаю schema.sql у меня закрывается соединение, поэтому закрываем и переоткрываем
conn.close()
conn = mysql.connector.connect(
    host="localhost",
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE
)



def user_exists(username):
    with conn.cursor() as cursor:
        query = "SELECT id FROM users WHERE username=%s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        return True if result else False


def item_exists(item_id):
    with conn.cursor() as cursor:
        query = "SELECT id FROM inventory WHERE id=%s"
        cursor.execute(query, (item_id,))
        result = cursor.fetchone()
        return True if result else False


def get_role(username):
    with conn.cursor() as cursor:
        query = "SELECT role FROM users WHERE username=%s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        return result[0]
    

def register(username,password):
    try:
        with conn.cursor() as cursor:
            query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            cursor.execute(query, (username,hash_pass(password)))
            conn.commit()
            return 0
    except Exception as e:
        return 1
    return 1


def hash_pass(password):
    password = password.encode('utf-8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed


def correct_pw(username,password):
    with conn.cursor() as cursor:
        cursor.execute("SELECT password FROM users WHERE username=%s", (username,))
        hashed = cursor.fetchone()[0].encode('utf-8')
        if bcrypt.checkpw(password.encode('utf-8'), hashed): return True
    return False


def get_owned_items(username):
    with conn.cursor() as cursor:
        query = "SELECT id, name, amount, item_condition FROM inventory WHERE owned_by = %s"
        user_id = get_id(username)
        cursor.execute(query,(user_id,))
        result = cursor.fetchall()
        return result


def get_all_items():
    with conn.cursor() as cursor:
        query = "SELECT id, name, amount, item_condition, owned_by FROM inventory"
        cursor.execute(query)
        result = cursor.fetchall()
        for idx, item in enumerate(result):
            item_id = item[0]
            name = item[1]
            amount = item[2]
            condition = item[3]
            owned_by = get_username(item[4])
            result[idx] = [item_id, name, amount, condition, owned_by]
        return result


def get_id(username):
    with conn.cursor() as cursor:
        query = "SELECT id FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        if result is None:
            return None
        return result[0]


def get_username(id):
    with conn.cursor() as cursor:
        query = "SELECT username FROM users WHERE id = %s"
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        if result is None:
            return None
        return result[0]

    
def add_item(name,amount,owned_by_username):
    try:
        with conn.cursor() as cursor:
            query = "INSERT INTO inventory (name,amount, owned_by) VALUES (%s,%s,%s)"
            user_id = get_id(owned_by_username)
            cursor.execute(query, (name,amount,user_id))
            conn.commit()
            return 0
    except Exception as e:
        return 1


def change_item(item_id, name, amount, condition, owned_by_username):
    try:
        with conn.cursor() as cursor:
            query = "UPDATE inventory SET name = %s, amount = %s, item_condition = %s, owned_by = %s WHERE id = %s"
            user_id = get_id(owned_by_username)
            cursor.execute(query,(name,amount,condition,user_id,item_id))
            conn.commit()
            return 0
    except Exception as e:
        print(e)
        return 1


def delete_item(item_id):
    try:
        with conn.cursor() as cursor:
            query = "DELETE FROM inventory WHERE id = %s"
            cursor.execute(query,(item_id,))
            conn.commit()
            return 0
    except Exception as e:
        print(e)
        return 1


def item_owned_by(item_id):
    with conn.cursor() as cursor:
        query = "SELECT owned_by FROM inventory WHERE id = %s"
        cursor.execute(query, (item_id,))
        result = cursor.fetchone()
        if result is None:
            return None
        return result[0]


def get_pending_fix_requests():
    with conn.cursor() as cursor:
        query = "SELECT id, user_id, item_id, request_status FROM fix_requests WHERE request_status = 'pending'"
        cursor.execute(query)
        result = cursor.fetchall()
        for idx, request in enumerate(result):
            request_id = request[0]
            username = get_username(request[1])
            item_id = request[2]
            request_status = request[3]
            result[idx] = [request_id, username, item_id, request_status]
        return result


def get_user_fix_requests(user_id):
    with conn.cursor() as cursor:
        query = "SELECT id, user_id, item_id, request_status FROM fix_requests WHERE user_id = %s"
        cursor.execute(query,(user_id,))
        result = cursor.fetchall()
        for idx, request in enumerate(result):
            request_id = request[0]
            username = get_username(request[1])
            item_id = request[2]
            request_status = request[3]
            result[idx] = [request_id, username, item_id, request_status]
        return result


def is_fix_request_pending(request_id):
    with conn.cursor() as cursor:
        query = "SELECT id FROM fix_requests WHERE id = %s"
        cursor.execute(query, (request_id,))
        result = cursor.fetchone()
        if result is None:
            return False
        return True
    return False


def approve_fix_request(request_id):
    with conn.cursor() as cursor:
        query = "UPDATE fix_requests SET request_status = 'approved' WHERE id = %s"
        cursor.execute(query,(request_id,))
        conn.commit()
        return 0
    return 1


def deny_fix_request(request_id):
    with conn.cursor() as cursor:
        query = "UPDATE fix_requests SET request_status = 'declined' WHERE id = %s"
        cursor.execute(query,(request_id,))
        conn.commit()
        return 0
    return 1


def create_fix_request(item_id, user_id):
    with conn.cursor() as cursor:
        query = "INSERT INTO fix_requests (user_id, item_id) VALUES (%s,%s)"
        cursor.execute(query, (user_id,item_id))
        conn.commit()
        return 0
    return 1


def get_pending_inventory_requests():
    with conn.cursor() as cursor:
        query = "SELECT id, user_id, message, request_status FROM inventory_requests WHERE request_status = 'pending'"
        cursor.execute(query)
        result = cursor.fetchall()
        for idx, request in enumerate(result):
            request_id = request[0]
            username = get_username(request[1])
            message = request[2]
            request_status = request[3]
            result[idx] = [request_id, username, message, request_status]
        return result

def get_user_inv_requests(user_id):
    with conn.cursor() as cursor:
        query = "SELECT id, user_id, message, request_status FROM inventory_requests WHERE user_id = %s"
        cursor.execute(query,(user_id,))
        result = cursor.fetchall()
        for idx, request in enumerate(result):
            request_id = request[0]
            username = get_username(request[1])
            message = request[2]
            request_status = request[3]
            result[idx] = [request_id, username, message, request_status]
        return result


def is_inventory_request_pending(request_id):
    with conn.cursor() as cursor:
        query = "SELECT id FROM inventory_requests WHERE id = %s AND request_status = 'pending'"
        cursor.execute(query, (request_id,))
        result = cursor.fetchone()
        if result is None:
            return False
        return True
    return False


def approve_inventory_request(request_id):
    with conn.cursor() as cursor:
        query = "UPDATE inventory_requests SET request_status = 'approved' WHERE id = %s"
        print(request_id)
        cursor.execute(query,(request_id,))
        conn.commit()
        return 0
    return 1


def deny_inventory_request(request_id):
    with conn.cursor() as cursor:
        query = "UPDATE inventory_requests SET request_status = 'declined' WHERE id = %s"
        print(request_id)
        cursor.execute(query,(request_id,))
        conn.commit()
        return 0
    return 1


def create_inventory_request(user_id, message):
    with conn.cursor() as cursor:
        query = "INSERT INTO inventory_requests (user_id, message) VALUES (%s,%s)"
        cursor.execute(query, (user_id,message))
        conn.commit()
        return 0
    return 1


def create_order(item_name, amount, price, supplier):
    with conn.cursor() as cursor:
        query = "INSERT INTO orders (name, amount, price, supplier) VALUES (%s,%s,%s,%s)"
        cursor.execute(query, (item_name,amount,price,supplier))
        conn.commit()
        return 0
    return 1


def change_order(order_id, name, amount, price, supplier):
    with conn.cursor() as cursor:
        query = "UPDATE orders SET item_name = %s, amount = %s, price = %s, supplier = %s WHERE id = %s"
        cursor.execute(query, (name, amount, price, supplier, order_id))
        conn.commit()
        return 0
    return 1

def get_orders():
    with conn.cursor() as cursor:
        query = "SELECT id, name, amount, price, supplier FROM orders"
        cursor.execute(query)
        result = cursor.fetchall()
        return result


def create_excel(data):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "report"
    headers = ['id','item name','amount','condition','owner']
    sheet.append(headers)

    for row in data:
        print(row)
        sheet.append(row)

    output = BytesIO()
    workbook.save(output)
    output.seek(0)
    return output


def autocomplete(usernameStart):
    with conn.cursor() as cursor:
        query = "SELECT username FROM users WHERE username LIKE %s ORDER BY username LIMIT 5"
        cursor.execute(query, (usernameStart+'%',))
        result = cursor.fetchall()
        return result