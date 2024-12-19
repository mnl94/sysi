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

cursor = conn.cursor()

with open('schema.sql', 'r') as file:
    sql = file.read()

# читаем схему и создаём таблицы
cursor.execute(sql, multi=True)


def valid_username(username):
    if len(username) > 255: return False
    for char in BLACKLISTED_CHARACTERS:
        if char in username: return False
    return True


def valid_password(password):
    if len(password) < 4: return False
    return True


def user_exists(username):
    query = "SELECT username FROM users WHERE username=%s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    return True if result else False


def get_role(username):
    query = "SELECT role FROM users WHERE username=%s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    return result[0]
    

def register(username,password):
    try:
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(query, (username,hash_pass(password)))
        conn.commit()
        return 0
    except Exception as e:
        return 1


def hash_pass(password):
    password = password.encode('utf-8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed


def correct_pw(username,password):
    cursor.execute("SELECT password FROM users WHERE username=%s", (username,))
    hashed = cursor.fetchone()[0].encode('utf-8')
    if bcrypt.checkpw(password.encode('utf-8'), hashed): return True
    return False



