# from app import app
from app import *
from app.database import *
from app.forms import *
from flask import render_template, redirect, send_from_directory, url_for, flash, request, Flask, session
from flask_login import login_user, logout_user, login_required, current_user
from app.routes.functions.mail import *
from app.routes.functions.user_content import * 
import sys, requests

@app.route('/fb_login')
def fb_login():
    redirect_uri = url_for('facebook_callback', _external=True)
    return redirect(f"https://www.facebook.com/v12.0/dialog/oauth?client_id={app.config['FACEBOOK_APP_ID']}&redirect_uri={redirect_uri}&scope=publish_actions")


@app.route('/facebook_callback')
def facebook_callback():
    code = request.args.get('code')
    redirect_uri = url_for('facebook_callback', _external=True)
    response = requests.get(f"https://graph.facebook.com/v12.0/oauth/access_token?client_id={app.config['FACEBOOK_APP_ID']}&redirect_uri={redirect_uri}&client_secret={app.config['FACEBOOK_APP_SECRET']}&code={code}")
    access_token = response.json()['access_token']
    session['access_token'] = access_token
    return redirect(url_for('post_on_facebook'))

@app.route('/post_on_facebook')
def post_on_facebook():
    if 'access_token' not in session:
        return redirect(url_for('fb_login'))
    message = "Hello, Facebook!"
    response = requests.post(f"https://graph.facebook.com/me/feed?message={message}&access_token={session['access_token']}")
    if response.status_code == 200:
        return "Posted successfully on Facebook!"
    else:
        return "Failed to post on Facebook."