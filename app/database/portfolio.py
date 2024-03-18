from app import db
from datetime import datetime
    
class Portfolio(db.Model):
    __tablename__ = 'portfolio'
    
    name = db.Column(db.String(50), nullable=False)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.String(1000), nullable=True)
    icon = db.Column(db.String(100), nullable=True)