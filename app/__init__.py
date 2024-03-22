from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from os import environ
import mysql.connector
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

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

creds = None
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
MAIL_USERNAME = environ.get('MAIL_USERNAME')
TOKEN_FILE_PATH = "/tmp/token.json"
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.

if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    # else:
    #     flow = InstalledAppFlow.from_client_secrets_file(
    #         "credentials.json", SCOPES
    #     )
    #     creds = flow.run_local_server(port=6900)
    
    # Save the credentials to the /tmp directory
    with open(TOKEN_FILE_PATH, "w") as token:
        token.write(creds.to_json())

try:
    # Call the Gmail API
    mail_client = build("gmail", "v1", credentials=creds)
    
except HttpError as error:
    # Handle errors from Gmail API
    print(f"An error occurred: {error}")

        
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
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))