from app import *
from app import db
from app.database import *
from app.forms import *
from flask import render_template, redirect, send_from_directory, url_for, flash, request, Response, jsonify
from flask_login import login_required, current_user
import sys
from .functions.openai import summarization, text_generation, image_generation, image_regeneration, text_regeneration
from app.routes.functions.mail import *
from app.routes.functions.imgur import *
from app.routes.functions.user_content import user_content

@app.route('/addCampaign', methods=['GET', 'POST'])
@login_required
def add_campaign():
    form = AddCampaignForm()
    
    if form.validate_on_submit():
        campaign = Campaign(
            user_id=current_user.id,
            name=form.campaign_name.data,
            links=form.links.data,
            perspective=form.perspective.data,
            portfolio_id = form.portfolio.data
        )
        db.session.add(campaign)
        db.session.commit()
        new_campaign = Campaign.query.filter_by(user_id = current_user.id).order_by(Campaign.creation_date.desc()).first()
        content = user_content(current_user.id)
        return redirect(url_for('generate_campaign', new_campaign_id = new_campaign.campaign_id, call_type = 'new', content=content))
    
    content = user_content(current_user.id)
    return render_template('addCampaign.html', form = form, content=content)

@app.route('/viewCampaign/<int:campaign_id>', methods=['GET', 'POST'])
@login_required
def view_campaign(campaign_id):
    campaign = Campaign.query.get(campaign_id)
    if campaign.user_id != current_user.id:
        message = "The user does not have permission to view this campaign!"
        return render_template('error.html', message=message)
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
        parent_id = campaign.parent_id

        campaign = [name, creation_date, links, summarization, perspective, text_generated, image_prompt, image_generated, id, portfolio_id, parent_id]

        # all_campaigns = Campaign.query.filter_by(parent_id = parent_id).order_by(Campaign.creation_date.desc()).all()
        # campaigns = []
        
        # for campaign in all_campaigns:
        #     name = campaign.name
        #     creation_date = campaign.creation_date
        #     links = campaign.links
        #     summarization = campaign.summarization
        #     perspective = campaign.perspective
        #     text_generated = campaign.text_generated
        #     image_prompt = campaign.image_prompt
        #     image_generated = campaign.image_generated
        #     id = campaign.campaign_id
        #     parent_id = campaign.parent_id
        #     campaigns.append((name, creation_date, links, summarization, perspective, text_generated, image_prompt, image_generated, id))

        content = user_content(current_user.id)
        return render_template('viewCampaign.html', campaign=campaign, content = content)

@app.route('/editCampaign/<int:campaign_id>', methods=['GET', 'POST'])
@login_required
def edit_campaign(campaign_id):
    campaign = Campaign.query.get(campaign_id)
    if campaign.user_id != current_user.id:
        message = "The user does not have permission to edit this campaign!"
        return render_template('error.html', message=message)
    else:
        form = EditCampaignForm()
        if form.validate_on_submit():            
            new_campaign = Campaign(
                user_id=current_user.id,
                name=form.campaign_name.data,
                links=form.links.data,
                perspective=form.perspective.data,
                parent_id = campaign.campaign_id,
                portfolio_id = campaign.portfolio_id
            )
            db.session.add(new_campaign)
            db.session.commit()

            new_campaign = Campaign.query.filter_by(user_id = current_user.id).order_by(Campaign.creation_date.desc()).first()
            content = user_content(current_user.id)
            return redirect(url_for('generate_campaign', new_campaign_id = new_campaign.campaign_id, call_type = 'edit', content=content))
    content = user_content(current_user.id)
    return render_template('editCampaign.html',campaign = campaign, form = form, content = content)


@app.route('/viewCampaigns', methods=['GET', 'POST'])
@login_required
def view_campaigns():
    call_type = request.args.get('call_type')
    id = request.args.get('id')
    
    if call_type == 'user':
        if int(id) != current_user.id:
            message = "The user does not have permission to view another user's campaigns!"
            return render_template('error.html', message=message)
        else:
            all_campaigns = Campaign.query.filter_by(user_id = id).order_by(Campaign.creation_date.desc()).all()
        
    elif call_type == 'portfolio':
        all_campaigns = Campaign.query.filter_by(portfolio_id = id).order_by(Campaign.creation_date.desc()).all()
        
    campaigns = []  
    row_campaigns = []
    count = 1
    
    for campaign in all_campaigns:
        c_name = campaign.name
        c_creation_date = campaign.creation_date
        text_generated = campaign.text_generated
        image_generated = campaign.image_generated
        id = campaign.campaign_id
        row_campaigns.append((c_name, c_creation_date, text_generated, image_generated, id))
        
        if count %4 == 0:
            campaigns.append(row_campaigns)
            row_campaigns = []    
        
        count += 1
        
    if count-1 %4 != 0:
        campaigns.append(row_campaigns)

    content = user_content(current_user.id)
    
    if call_type == 'user':
        return render_template('viewCampaigns.html', campaigns=campaigns, content=content)
        
    elif call_type == 'portfolio':
        return render_template('viewPortfolio.html', campaigns=campaigns, content=content)

@app.route('/generateCampaign', methods=['GET', 'POST'])
@login_required
def generate_campaign():
    new_campaign_id = int(request.args.get('new_campaign_id'))
    call_type = request.args.get('call_type')
    new_campaign = Campaign.query.get(new_campaign_id)
    content = user_content(current_user.id)
    return render_template('generateCampaign.html', new_campaign_id = new_campaign_id, new_campaign = new_campaign, call_type = call_type, content=content)

@app.route('/createCampaign/<int:new_campaign_id>/<call_type>', methods=['GET', 'POST'])
@login_required
def create_campaign(new_campaign_id, call_type):
    new_campaign = Campaign.query.get(new_campaign_id)
    if call_type == 'edit':
        old_campaign = Campaign.query.get(new_campaign.parent_id)
    elif call_type == 'new':
        old_campaign = new_campaign
        
    def generation_function(new_campaign, call_type):
        name = new_campaign.name
        links = new_campaign.links
        perspective = new_campaign.perspective
        
        if call_type == 'new':
            summary = ''
            for chunk in summarization(links):
                yield f"event: summary\ndata: {chunk}\n\n"
                summary += chunk
                
            ad_text = ''
            for chunk in text_generation(summary, perspective):
                yield f"event: ad_text\ndata: {chunk}\n\n"
                ad_text += chunk
            
            img_prompt = "Generate an image **NOT containing text** that captures the spirit of the following text: " + ad_text
            image_url = image_generation(img_prompt)
            
            yield f"event: img_url\ndata: {image_url}\n\n"
            yield f"event: campaign_id\ndata: {new_campaign.campaign_id}\n\n"
                
        elif call_type == 'edit':
            summary = old_campaign.summarization
            ad_text = old_campaign.text_generated
            img_prompt = old_campaign.image_prompt
            image_url = old_campaign.image_generated
        
            if links != old_campaign.links:
                summary = ''
                for chunk in summarization(links):
                    yield f"event: summary\ndata: {chunk}\n\n"
                    summary += chunk
                    
                ad_text = ''
                for chunk in text_generation(summary, perspective):
                    yield f"event: ad_text\ndata: {chunk}\n\n"
                    ad_text += chunk
                    
                img_prompt = "Generate an image **NOT containing text** that captures the spirit of the following text: " + ad_text
                image_url = image_generation(img_prompt)
                
                yield f"event: img_url\ndata: {image_url}\n\n"
                yield f"event: campaign_id\ndata: {new_campaign.campaign_id}\n\n"
                
            elif perspective != old_campaign.perspective:
                summary_chunks = summary.split()
                for chunk in summary_chunks:
                    yield f"event: summary\ndata: {chunk + ' '}\n\n"
                
                ad_text = ''
                for chunk in text_generation(summary, perspective):
                    yield f"event: ad_text\ndata: {chunk}\n\n"
                    ad_text += chunk
                
                img_prompt = "Generate an image **NOT containing text** that captures the spirit of the following text: " + ad_text
                image_url = image_generation(img_prompt)
                
                yield f"event: img_url\ndata: {image_url}\n\n"
                yield f"event: campaign_id\ndata: {new_campaign.campaign_id}\n\n"
            
            else:
                summary_chunks = summary.split()
                for chunk in summary_chunks:
                    yield f"event: summary\ndata: {chunk + ' '}\n\n"
                    
                ad_text_chunks = ad_text.split()
                for chunk in ad_text_chunks:
                    yield f"event: ad_text\ndata: {chunk + ' '}\n\n"
                
                yield f"event: img_url\ndata: {image_url}\n\n"
                yield f"event: campaign_id\ndata: {new_campaign.campaign_id}\n\n"  
        
        yield f"event: final_summary\ndata: {summary}\n\n" 
        yield f"event: final_ad_text\ndata: {ad_text}\n\n"
        yield f"event: final_img_prompt\ndata: {img_prompt}\n\n"
        yield f"event: final_img_url\ndata: {image_url}\n\n"
        
        if call_type == 'new':
            yield f"event: final_parent_id\ndata: {new_campaign.campaign_id}\n\n"
                
        elif call_type == 'edit':
            yield f"event: final_parent_id\ndata: {old_campaign.campaign_id}\n\n"
            
        yield f"data: end-of-stream\n\n"
        
    response_stream = generation_function(new_campaign, call_type)
    return Response(response_stream, content_type="text/event-stream")
                    
@app.route('/processCampaign', methods=['POST'])
@login_required
def process_campaign():
    data = request.get_json()

    new_campaign_id = int(data['new_campaign_id'])
    call_type = data['call_type']
    summary = data['summary']
    ad_text = data['ad_text']
    img_prompt = data['img_prompt']
    image_url = data['image_url']
    parent_id = int(data['parent_id'])
    
    new_campaign = Campaign.query.get(new_campaign_id)
    old_campaign = Campaign.query.get(parent_id)
    
    imgur_link = image_upload(image_url)
    
    new_campaign.summarization = summary
    new_campaign.text_generated = ad_text
    new_campaign.image_prompt = img_prompt
    new_campaign.image_generated = imgur_link
    new_campaign.parent_id = parent_id

    if call_type == 'new':
        campaign_creation_notification(current_user, new_campaign)
        
    elif call_type == 'edit':
        campaign_edit_notification(current_user, old_campaign, new_campaign)
    
    db.session.commit()
    return jsonify({'message': 'Campaign processed successfully'})

@app.route('/regenerateImage', methods=['GET','POST'])
@login_required
def regenerate_image():
    data = request.get_json()
    img_url = data['img_url']
    feedback = data['feedback']
    new_img = image_regeneration(feedback, img_url)
    return jsonify({'new_image_url': new_img})

@app.route('/regenerateSummarization', methods=['GET','POST'])
@login_required
def regenerate_summarization():
    prompt = request.args.get('summarization', '')
    feedback = request.args.get('feedback', '')
    
    def regeneration_function(prompt, feedback):
        summary = ''
        for chunk in text_regeneration(prompt, feedback):
            yield f"event: summary\ndata: {chunk}\n\n"
            summary += chunk
                
        yield f"event: final_summary\ndata: {summary}\n\n" 
        yield f"data: end-of-stream\n\n"
        
    response_stream = regeneration_function(prompt, feedback)
    return Response(response_stream, content_type="text/event-stream")

@app.route('/regenerateAdvertisement', methods=['GET','POST'])
@login_required
def regenerate_advertisement():
    prompt = request.args.get('ad_text', '')
    feedback = request.args.get('feedback', '')
    
    def regeneration_function(prompt, feedback):
        ad_text = ''
        for chunk in text_regeneration(prompt, feedback):
            yield f"event: ad_text\ndata: {chunk}\n\n"
            ad_text += chunk      
        
        yield f"event: final_ad_text\ndata: {ad_text}\n\n"
        yield f"data: end-of-stream\n\n"
        
    response_stream = regeneration_function(prompt, feedback)
    return Response(response_stream, content_type="text/event-stream")