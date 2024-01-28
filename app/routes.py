from app import app
from flask import render_template, redirect, send_from_directory, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import *
import sys
from flask_mail import Mail, Message
import smtplib
import plotly.express as px
from plotly.offline import plot
from plotly.offline import *
import plotly.graph_objs as go
import pandas as pd

# mail send
mail = Mail(app)

# Replace these values with your email credentials
# Create project-specific email, get API email key
EMAIL_USER = 'jonathanwarren2022@gmail.com'
EMAIL_PASSWORD = ''

def send_mail(addr, msg):
    recipient = addr
    subject = 'Test Flask email'
    message = Message(subject, recipients=[recipient], body = msg)
    mail.send(message)

def serve_static(path):
    return send_from_directory('static', path)

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/home')
@login_required
def index():
    if current_user.newuser == True:
        flash('Complete the "New Users" Section!', 'success')
        
    # campaigns = view_campaigns()
    # campaign_info = []
    return render_template('index.html')

@app.route('/login', methods = ['GET', 'POST'])
def signin():
    email = request.form['email']
    password = request.form['password']
    user = db.session.query(User).filter_by(email=email).first()
    
    if user is None or not user.check_password(password):
        print(f'Login failed for user: {user.first_name} {user.last_name}', file=sys.stderr)
        print(f'Provided email: {email}', file=sys.stderr)
        print(f'Provided password: {password}', file=sys.stderr)
        print(f'User object: {user}', file=sys.stderr)
        flash('An error occurred when trying to sign-in', 'success')
        return redirect(url_for('landing'))

    login_user(user)
    flash('Login Successful!', 'success')
    # print('Login successful', file=sys.stderr)
    return redirect(url_for('index'))
    

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Read data from form fields
    user_name = request.form['username']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    password_verification = request.form['password_verification']
        
    user = db.session.query(User).filter_by(email=email).first()
    
    if user is None:
        if password == password_verification:
            # Create new user object and add to database
            user = User(username=user_name,first_name=first_name, last_name=last_name, email=email, newuser = True)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            
            print('Sign-up successful', file=sys.stderr)
            
            # email notification of sign-up
            # ACCT_EMAIL = email
            # try:
            #     server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            #     server.login(EMAIL_USER, EMAIL_PASSWORD)

            #     body = f"Subject: Account Created\n\nWelcome to the Finance Tracker, {first_name} {last_name}! Your account information is listed below: \nName: {first_name} {last_name}\nEmail: {email}"
            #     server.sendmail(EMAIL_USER, ACCT_EMAIL, body)

            #     server.quit()
            
            # except Exception as e:
            #     return f"Error: {e}" 
            
            flash('Account Created!', 'success')
            return redirect(url_for('landing'))
        
        else:
            flash('An error occurred when trying to sign-up', 'success')
            return redirect(url_for('landing'))

    else:
        # account already created with email.
        print(f'Error: Signup failed for user: {first_name} {last_name}', file=sys.stderr)
        print(f'Provided email: {email} is already being used for an account.', file=sys.stderr)
        flash('An error occurred when trying to sign-up', 'success')
        return redirect(url_for('landing'))
    
@app.route('/newuser', methods=['GET', 'POST'])
@login_required
def new_user():
    if current_user.newuser == True:
        print('new user.')
    else:
        print('not new user.')
    
    return redirect(url_for('index'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been successfully logged out.', 'success')
    return redirect(url_for('landing'))

@app.route('/changepassword', methods=['GET', 'POST'])
@login_required
def change_password():     
    new_password = request.form['new_password']
    password_retype = request.form['password_retype']
        
    if new_password != password_retype:
        flash('Passwords do not match.', 'danger')
    else:
        new_password_hash = generate_password_hash(new_password)
        current_user.password = new_password_hash
        db.session.commit()
        flash('Your password has been updated. Please sign in again.', 'success')
        
        # Log user out after changing the password
        logout_user()
        return redirect(url_for('landing'))
    
    return redirect(url_for('index'))

@app.route('/addcampaign', methods=['GET', 'POST'])
@login_required
def add_campaign():
 
    if current_user.newuser == True:
        amount = request.form['amount']
        campaign = campaign(user_id = current_user.id, 
                                title = "Initial Amount", 
                                date = "1/1/2000", 
                                amount = amount, 
                                type = 'deposit', 
                                category = "deposit", 
                                comments = "initial starting balance")
        db.session.add(campaign)
        current_user.newuser == False
 
    else:
        title = request.form['title']
        date = request.form['date']
        amount = request.form['amount']
        payment_id = request.form['card']
        if payment_id == '':
            payment_id = None
        type = request.form['type']
        category = request.form['category']
        comments = request.form['comments']
            
        # Add campaign to database
        campaign = campaign(user_id = current_user.id,
                                    payment_id = payment_id, 
                                    title = title, 
                                    date = date, 
                                    amount = amount, 
                                    type = type, 
                                    category = category, 
                                    comments = comments)
        
        db.session.add(campaign)
        
    db.session.commit()
        
    ACCT_EMAIL = current_user.email
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(EMAIL_USER, EMAIL_PASSWORD)

        body = f"Subject: campaign Added\n\n A campaign has been added to your account: \nTitle: {title}\nDate: {date}\n Amount: {amount} \nType: {type}\nCategory: {category} \nComments: {comments} \n has been added to your account."
        server.sendmail(EMAIL_USER, ACCT_EMAIL, body)

        server.quit()
    
    except Exception as e:
        return f"Error: {e}" 

    flash('campaign Added!', 'success')
    return redirect(url_for('index'))

    
def view_campaigns():
    all_campaigns = Campaign.query.order_by(Campaign.id).filter_by(user_id=current_user.id).all()

    return all_campaigns


@app.route('/viewCampaign/<int:campaign_id>', methods=['GET', 'POST'])
@login_required
def campaignDetails(campaign_id):
    campaign = campaign.query.filter_by(id=campaign_id).first()
    print(campaign)
    return render_template('index.html')

@app.route('/deleteCampaign/<int:campaign_id>', methods=['GET', 'POST'])
@login_required
def DeleteCampaign(campaign_id):
    print('delete Campaign')

    return render_template('index.html')

@app.route('/updateCampaign/<int:campaign_id>', methods=['GET', 'POST'])
@login_required
def UpdateCampaign(campaign_id):
    print('update Campaign')

    return render_template('index.html')