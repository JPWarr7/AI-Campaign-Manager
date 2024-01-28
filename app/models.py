from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    
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

class Campaign(db.Model):
    __tablename__ = 'campaign'
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'))
    campaign_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(1000), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    POV = db.Column(db.String(1000), nullable=False)
    resources = db.Column(db.String(1000), nullable=False)
    image_prompt = db.Column(db.String(1000), nullable=False)
    
    text_generated = db.Column(db.String(1000), nullable=False)
    
    # images_generated = 
    
    
    # research necessary for images_generated and output - storing images 
    # in database is slow and unnecessary, can be stored externally and 
    # instead we can store a link to the image here in this field. 
    
class Portfolio(db.Model):
    __tablename__ = 'portfolio'
    
    title = db.Column(db.String(50), nullable=False)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    

    