from app import db
from app.models import User
import pandas as pd

def populate_db():
    # create a few users
    users = [
        ('jpwarr', 'jp', 'warr','jonathanwarren2022@gmail.com', '123')
        ]
    
    for username, first_name, last_name, email, password in users:
        user = User(username = username, first_name = first_name, last_name=last_name, email=email, password=password)
        user.set_password(password)
        db.session.add(user)
    db.session.commit()
