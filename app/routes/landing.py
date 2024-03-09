# from app import app
from app import *
from flask import render_template, redirect, send_from_directory, url_for, flash, request
from app import *
from flask_login import login_user, logout_user, login_required, current_user
from app import app
# from app import db
# from app.database import *
# import sys
# from flask_mail import Mail, Message
# import smtplib
# import plotly.express as px
# from plotly.offline import plot
# from plotly.offline import *
# import plotly.graph_objs as go
# import pandas as pd

def serve_static(path):
    return send_from_directory('static', path)

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('home.html')
    # return render_template('viewCampaigns.html', call_type = 'user', id = current_user.id)