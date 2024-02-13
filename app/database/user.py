from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    
    # social media accounts - placeholder boolean for now. API + research
    # necessary to connect social media acct. to our database
    facebook = db.Column(db.Boolean)
    twitter = db.Column(db.Boolean)
    instagram = db.Column(db.Boolean)
    tiktok = db.Column(db.Boolean)
    
    newuser = db.Column(db.Boolean)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def is_active(self):
        # return True if the user is active
        return True
    
    def get_id(self):
        return str(self.id)

    @property
    def is_authenticated(self):
        return True