# from app import app
from app import *
from app.database import *
from app.forms import *
from flask import render_template, redirect, send_from_directory, url_for, flash, request, Flask, session
from app.routes.functions.mail import *
from app.routes.functions.user_content import * 
import sys, requests


# portfolio = Portfolio.query.filter_by(user_id=current_user.id).order_by(Portfolio.creation_date.desc()).first()

@app.route('/feed')
def feed():
    all_campaigns = Campaign.query.filter_by(public=True).order_by(Campaign.creation_date.desc()).all()
    users=[]
    campaigns=[]
    for campaign in all_campaigns:
        user = User.query.get(campaign.user_id)
        users.append(user)
        campaigns.append(campaign)
        
    feed = zip(campaigns, users)
    content = user_content(current_user.id)
    return render_template('feed.html', feed=feed, content=content)

@app.route('/facebook/login')
def fb_login():
    redirect_uri = url_for('facebook_callback', _external=True)
    return redirect(f"https://www.facebook.com/v12.0/dialog/oauth?client_id={app.config['FACEBOOK_APP_ID']}&redirect_uri={redirect_uri}&scope=publish_actions")


@app.route('/facebook/callback')
def facebook_callback():
    code = request.args.get('code')
    redirect_uri = url_for('facebook_callback', _external=True)
    response = requests.get(f"https://graph.facebook.com/v12.0/oauth/access_token?client_id={app.config['FACEBOOK_APP_ID']}&redirect_uri={redirect_uri}&client_secret={app.config['FACEBOOK_APP_SECRET']}&code={code}")
    access_token = response.json()['access_token']
    session['access_token'] = access_token
    return redirect(url_for('post_on_facebook'))

@app.route('/facebook/post')
def post_on_facebook():
    if 'access_token' not in session:
        return redirect(url_for('fb_login'))
    message = "Hello, Facebook!"
    response = requests.post(f"https://graph.facebook.com/me/feed?message={message}&access_token={session['access_token']}")
    if response.status_code == 200:
        return "Posted successfully on Facebook!"
    else:
        return "Failed to post on Facebook."