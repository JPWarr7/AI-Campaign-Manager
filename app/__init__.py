from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from dotenv import load_dotenv
from os import environ
import mysql.connector

# Force loading of environment variables
load_dotenv('.flaskenv')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'JPWarr'

IP = environ.get('MYSQL_IP')
USERNAME = environ.get('MYSQL_USER')
PASSWORD = environ.get('MYSQL_PASS')
DB_NAME = environ.get('MYSQL_DB')


# Specify the connection parameters/credentials for the database
DB_CONFIG_STR = f"mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{IP}/{DB_NAME}"
app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONFIG_STR
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True

# Create database connection and associate it with the Flask application
db = SQLAlchemy(app)
# Import the User model after creating the db object
from app.database import *

# Add login manager
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# # Specify mail environment variables
# MAIL_USERNAME = environ.get('MAIL_USERNAME')
# MAIL_APP_PASSWORD = environ.get('MAIL_APP_PASSWORD')
# MAIL_SENDER_NAME = environ.get('MAIL_SENDER_NAME')

# # Setup mail client
# app.config.update(
#         MAIL_SERVER = 'smtp.gmail.com',
#         MAIL_PORT = 465,
#         MAIL_USE_TLS = False,
#         MAIL_USE_SSL = True,
#         MAIL_USERNAME = MAIL_USERNAME,
#         MAIL_PASSWORD = MAIL_APP_PASSWORD,
#         MAIL_DEFAULT_SENDER = (MAIL_SENDER_NAME, MAIL_USERNAME)
#         )

# mail = Mail(app)

# Add models
from app.routes import *
from app.forms import *
# from app import database

# with app.app_context():
#     try:
#         db.drop_all()
#         db.create_all()
# #         populate_db()
#     except Exception as e:
#         print("Error:", e)

        
# Populate database

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)