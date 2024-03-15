from app import *
from app import db
from app.database import *
from app.forms import *
from flask import render_template, redirect, send_from_directory, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
import sys
from app.routes.functions.mail import *
from app.routes.functions.user_content import *


@app.route('/addPortfolio', methods=['GET', 'POST'])
@login_required
def add_portfolio():
    form = AddPortfolioForm()
    
    if form.validate_on_submit():
        portfolio = Portfolio(
            user_id=current_user.id,
            name=form.portfolio_name.data
        )
        db.session.add(portfolio)
        db.session.commit()
        portfolio = Portfolio.query.filter_by(user_id = current_user.id).order_by(Portfolio.creation_date.desc()).first()
        portfolio_creation_notification(current_user, portfolio)
        content = user_content(current_user.id)
        return redirect(url_for('view_portfolio', portfolio_id = portfolio.id, content=content))
    
    content = user_content(current_user.id)
    return render_template('addPortfolio.html', form=form, content=content)

@app.route('/viewPortfolio/<int:portfolio_id>', methods=['GET', 'POST'])
@login_required
def view_portfolio(portfolio_id):
    portfolio = Portfolio.query.get(portfolio_id)
    name = portfolio.name
    creation_date = portfolio.creation_date
    
    all_campaigns = Campaign.query.filter_by(portfolio_id = portfolio.id).order_by(Campaign.creation_date.desc()).all()
    
    final_campaigns = []    
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
            final_campaigns.append(row_campaigns)
            row_campaigns = []    
        
        count += 1
        
    if count-1 %4 != 0:
        final_campaigns.append(row_campaigns)

    content = user_content(current_user.id)
    portfolio = [name, creation_date, final_campaigns]
    return render_template('viewPortfolio.html', portfolio=portfolio, content=content)


@app.route('/editPortfolio/<int:portfolio_id>', methods=['GET', 'POST'])
@login_required
def edit_portfolio(portfolio_id):
    form = EditPortfolioForm()
    portfolio = Portfolio.query.get(portfolio_id)
    
    if form.validate_on_submit():
        if form.portfolio_name:
            portfolio.name=form.portfolio_name.data
        
        db.session.commit()
        content = user_content(current_user.id)
        return redirect(url_for('view_portfolio',portfolio_id = portfolio.id, content=content))
    content = user_content(current_user.id)
    return render_template('editPortfolio.html', content=content, form=form, portfolio=portfolio)

@app.route('/viewPortfolios', methods=['GET', 'POST'])
@login_required
def view_portfolios():
    all_portfolios = Portfolio.query.filter_by(user_id = current_user.id).all()
    portfolios = []
    
    for portfolio in all_portfolios:
        name = portfolio.name
        creation_date = portfolio.creation_date
        portfolio_id = portfolio.id
        portfolios.append((name, creation_date, portfolio_id))
    
    content = user_content(current_user.id)
    return render_template('viewPortfolios.html', portfolios=portfolios, content=content)
