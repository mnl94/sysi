import os
import bcrypt
from dotenv import load_dotenv
import mysql.connector

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

cursor = conn.cursor()

with open('schema.sql', 'r') as file:
    sql = file.read()

# читаем схему и создаём таблицы
cursor.execute(sql, multi=True)


def valid_username(username):
    return True


def valid_password(password):
    return True


def user_exists(username):
    return True
    

def get_role(role):
    return 'admin'
    

def register(username,password):
    return 0


def hash_pass(password):
    password = password.encode('utf-8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed
