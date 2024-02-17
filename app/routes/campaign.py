from app import *
from app import db
from app.database import *
from app.forms import *
from flask import render_template, redirect, send_from_directory, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
import sys
from .functions.openai import summarization, text_generation, image_generation

@app.route('/addCampaign', methods=['GET', 'POST'])
@login_required
def add_campaign():
    form = AddCampaignForm() 
    if form.validate_on_submit():
        links = form.links.data
        perspective = form.perspective.data
        summary = summarization(links)
        text_advertisement = text_generation(summary, perspective)
        img_prompt = "Generate an image capturing the spirit of the following text" + text_advertisement
        image_url = image_generation(img_prompt)
        
        campaign = Campaign(
            user_id=current_user.id,
            name=form.campaign_name.data,
            links=form.links.data,
            perspective=form.perspective.data,
            summarization = summary,
            text_generated = text_advertisement,
            image_prompt = img_prompt,
            image_generated = image_url
        )
        db.session.add(campaign)
        db.session.commit()
        campaign = Campaign.query.filter_by(user_id = current_user.id).order_by(Campaign.creation_date.desc()).first()
        campaign.parent_id = campaign.campaign_id
        db.session.commit()
        return redirect(url_for('view_campaign', campaign_id=campaign.campaign_id))
    
    return render_template('addCampaign.html', form = form)

@app.route('/viewCampaign/<int:campaign_id>', methods=['GET', 'POST'])
@login_required
def view_campaign(campaign_id):
    campaign = Campaign.query.get(campaign_id)
    all_campaigns = Campaign.query.filter_by(parent_id = campaign.parent_id).order_by(Campaign.creation_date.desc()).all()
    campaigns = []
    
    for campaign in all_campaigns:
        name = campaign.name
        creation_date = campaign.creation_date
        links = campaign.links
        summarization = campaign.summarization
        perspective = campaign.perspective
        text_generated = campaign.text_generated
        image_prompt = campaign.image_prompt
        image_generated = campaign.image_generated
        id = campaign.campaign_id
        campaigns.append((name, creation_date, links, summarization, perspective, text_generated, image_prompt, image_generated, id))

    return render_template('viewCampaigns.html', campaigns = campaigns)

@app.route('/editCampaign/<int:campaign_id>', methods=['GET', 'POST'])
@login_required
def edit_campaign(campaign_id):
    form = EditCampaignForm()
    campaign = Campaign.query.get(campaign_id)
    
    if form.validate_on_submit():
        if form.campaign_name:
            campaign_name=form.campaign_name.data
            
        if form.links:
            links=form.links.data
            
        # if form.text_summarization:
        #     summary=form.text_summarization.data
            
        if form.perspective:
            perspective=form.perspective.data
        
        # if form.text_generation:
        #     text_generated = form.text_generation.data
            
        # if form.image_prompt:
        #     image_prompt = form.image_prompt.data
            
        # if form.image_generation:
        #     image_generated = form.image_generation.data
        
        summary = summarization(links)
        text_advertisement = text_generation(summary, perspective)
        img_prompt = "Generate an image capturing the spirit of the following text" + text_advertisement
        image_url = image_generation(img_prompt)
        
        new_campaign = Campaign(
            user_id=current_user.id,
            name=campaign_name,
            links=links,
            perspective=perspective,
            summarization = summary,
            text_generated = text_advertisement,
            image_prompt = img_prompt,
            image_generated = image_url,
            parent_id = campaign.parent_id
        )
        db.session.add(new_campaign)
        db.session.commit()
        
        campaign = Campaign.query.filter_by(user_id = current_user.id).order_by(Campaign.creation_date.desc()).first()
        return redirect(url_for('view_campaign', campaign_id=campaign.campaign_id))
    
    return render_template('editCampaign.html',campaign = campaign, form = form)

@app.route('/viewCampaigns', methods=['GET', 'POST'])
@login_required
# def view_campaigns(call_type, id):
def view_campaigns():
    call_type = 'user'
    id = current_user.id
    if call_type == 'user':
        all_campaigns = Campaign.query.filter_by(user_id = id).all()
        
    elif call_type == 'portfolio':
        all_campaigns = Campaign.query.filter_by(portfolio_id = id).all()
        
    campaigns = []
    
    for campaign in all_campaigns:
        name = campaign.name
        creation_date = campaign.creation_date
        links = campaign.links
        summarization = campaign.summarization
        perspective = campaign.perspective
        text_generated = campaign.text_generated
        image_prompt = campaign.image_prompt
        image_generated = campaign.image_generated
        id = campaign.campaign_id
        campaigns.append((name, creation_date, links, summarization, perspective, text_generated, image_prompt, image_generated, id))

    if call_type == 'user':
        return render_template('viewCampaigns.html', campaigns=campaigns)
        
    elif call_type == 'portfolio':
        return render_template('viewPortfolio.html', campaigns=campaigns)
