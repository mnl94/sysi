import os
from dotenv import load_dotenv
import mysql.connector
from funcs import hash_pass

load_dotenv()

MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

# Подключение к базе данных
conn = mysql.connector.connect(
    host="localhost",
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE
)

with conn.cursor() as cursor:
    try:
        with open('schema.sql', 'r') as f:
            sql = " ".join(f.readlines())

        for res in cursor.execute(sql, multi=True):
            pass
        print('tables created')
    except Exception as e:
        print('Error while creating tables:', e)

with conn.cursor() as cursor:
    try:
        query = "INSERT INTO users (username, password, role) VALUES (%s, %s, 'admin')"
        cursor.execute(query, (ADMIN_USERNAME,hash_pass(ADMIN_PASSWORD)))
        conn.commit()
        print('admin created')
    except Exception as e:
        print('Error while creating admin user:   ',e)

conn.close()