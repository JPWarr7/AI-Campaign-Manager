from app import *
from app import db
from app.database import *


def user_content(user_id):
    all_portfolios = Portfolio.query.filter_by(user_id = user_id).order_by(Portfolio.creation_date.desc()).all()
    all_campaigns = Campaign.query.filter_by(user_id = user_id).order_by(Campaign.creation_date.desc()).all()
    
    campaigns = []
    portfolios = []
    content = []
    for campaign in all_campaigns:
        if campaign.image_generated is None:
            db.session.delete(campaign)
        else:
            name = campaign.name
            creation_date = campaign.creation_date
            links = campaign.links
            summarization = campaign.summarization
            perspective = campaign.perspective
            text_generated = campaign.text_generated
            image_prompt = campaign.image_prompt
            image_generated = campaign.image_generated
            id = campaign.campaign_id
            portfolio_id = campaign.portfolio_id
            campaigns.append((name, creation_date, links, summarization, perspective, text_generated, image_prompt, image_generated, id, portfolio_id))
            
    
    for portfolio in all_portfolios:
        name = portfolio.name
        creation_date = portfolio.creation_date
        id = portfolio.id
        portfolios.append((name, creation_date, id))
    
    db.session.commit()
    content.append(portfolios)
    content.append(campaigns)
    return content