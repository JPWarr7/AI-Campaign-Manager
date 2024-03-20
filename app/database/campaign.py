from app import db
from datetime import datetime
from sqlalchemy.orm import relationship


class Campaign(db.Model):
    __tablename__ = 'campaign'
  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id', ondelete='CASCADE'))
    campaign_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    parent_id = db.Column(db.Integer)
    name = db.Column(db.String(1000), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  
    links = db.Column(db.String(1000))
    summarization = db.Column(db.String(2500))
    perspective = db.Column(db.String(2500))
    text_generated = db.Column(db.String(2500))
    image_prompt = db.Column(db.String(2500))
    image_generated = db.Column(db.String(1000))