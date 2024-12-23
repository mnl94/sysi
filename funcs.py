import os
import bcrypt
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

BLACKLISTED_CHARACTERS = ['$', '%', '@', '#', '&', '*', '!', '(', ')', '+', '=', '{', '}', '[', ']', ';', ':', ' ']

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



def valid_username(username):
    if len(username) > 255: return False
    for char in BLACKLISTED_CHARACTERS:
        if char in username: return False
    return True


def valid_password(password):
    if len(password) < 4: return False
    return True


def user_exists(username):
    with conn.cursor() as cursor:
        query = "SELECT username FROM users WHERE username=%s"
        cursor.execute(query, (username,))
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
        query = "SELECT name, amount, item_condition FROM inventory WHERE owned_by = %s"
        id = get_id(username)
        cursor.execute(query,(id,))
        result = cursor.fetchall()
        return result


def get_all_items():
    with conn.cursor() as cursor:
        query = "SELECT name, amount, item_condition, owned_by FROM inventory"
        cursor.execute(query)
        result = cursor.fetchall()
        for idx, item in enumerate(result):
            name = item[0]
            amount = item[1]
            condition = item[2]
            owned_by = get_username(item[3])
            result[idx] = [name,amount,condition,owned_by]
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

    
def add_item(name,amount):
    try:
        with conn.cursor() as cursor:
            query = "INSERT INTO inventory (name,amount) VALUES (%s,%s)"
            cursor.execute(query, (name,amount))
            conn.commit()
            return 0
    except Exception as e:
        return 1
