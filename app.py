from flask import Flask, render_template, session
from api import api_blueprint
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.register_blueprint(api_blueprint, url_prefix='/api')

@app.route('/')
def main_html():
    return render_template('index.html')

@app.route('/login')
def login_html():
    return render_template('login.html')

@app.route('/register')
def register_html():
    return render_template('register.html')
    
@app.route('/inventory')
def inventory_html():
    role = session.get('role')
    if role == 'admin':
        return render_template('inventory.html')
    return '<html> Not admin </html>', 401

if __name__ == '__main__':
    app.run(debug=True)

