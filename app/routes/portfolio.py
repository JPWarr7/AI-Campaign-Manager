from app import *
from app import db
from app.database import *
from app.forms import *
from flask import render_template, redirect, send_from_directory, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
import sys
from app.routes.functions.mail import *
from app.routes.functions.user_content import *
from app.routes.functions.imgur import *

@app.route('/addPortfolioForm')
@login_required
def get_add_portfolio_form():
    form = AddPortfolioForm()
    return render_template('addPortfolio.html', form=form)

@app.route('/addPortfolio', methods=['POST'])
@login_required
def add_portfolio():
    form = AddPortfolioForm()
    if form.validate_on_submit():
        icon_file = request.files['icon']
        if icon_file:
            image_link = upload_image_from_file(icon_file)
        else:
            image_link = None
            flash('Invalid image file format. Please upload a valid image file.', 'error')
            
        portfolio = Portfolio(
            user_id=current_user.id,
            name=form.portfolio_name.data,
            description=form.description.data,
            icon=image_link
        )
        
        db.session.add(portfolio)
        db.session.commit()
        portfolio = Portfolio.query.filter_by(user_id=current_user.id).order_by(Portfolio.creation_date.desc()).first()
        portfolio_creation_notification(current_user, portfolio)
        return redirect(url_for('view_portfolio', portfolio_id=portfolio.id))

    return "Form validation failed"

@app.route('/viewPortfolio/<int:portfolio_id>', methods=['GET', 'POST'])
@login_required
def view_portfolio(portfolio_id):
    portfolio = Portfolio.query.get(portfolio_id)
    name = portfolio.name
    creation_date = portfolio.creation_date
    description = portfolio.description
    icon = portfolio.icon
    
    all_campaigns = Campaign.query.filter_by(portfolio_id = portfolio.id).order_by(Campaign.creation_date.desc()).all()
    
    final_campaigns = []    
    row_campaigns = []
    count = 2
    row_campaigns.append(('','','','','add'))
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
    portfolio = [name, creation_date, description, icon, final_campaigns]
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
        return redirect(url_for('view_portfolio',portfolio_id = portfolio.id))
    content = user_content(current_user.id)
    return render_template('editPortfolio.html', content=content, form=form, portfolio=portfolio)

@app.route('/viewPortfolios', methods=['GET', 'POST'])
@login_required
def view_portfolios():
    all_portfolios = Portfolio.query.filter_by(user_id = current_user.id).order_by(Portfolio.creation_date.desc()).all()
    portfolios = []
    campaigns = []
    for portfolio in all_portfolios:
        campaigns = []
        name = portfolio.name
        creation_date = portfolio.creation_date
        portfolio_id = portfolio.id
        icon = portfolio.icon
        description = portfolio.description
        
        all_campaigns = Campaign.query.filter_by(portfolio_id = portfolio.id).order_by(Campaign.creation_date.desc()).all()
        for campaign in all_campaigns:
            campaigns.append(campaign.image_generated)
            
        portfolios.append((name, creation_date, portfolio_id, icon, description, campaigns))
    
    content = user_content(current_user.id)
    return render_template('viewPortfolios.html', portfolios=portfolios, content=content)

@app.route('/deletePortfolio/<int:portfolio_id>', methods=['GET', 'POST'])
@login_required
def delete_portfolio(portfolio_id):
    portfolio = Portfolio.query.get(portfolio_id)
    if portfolio.user_id != current_user.id:
        message = "The user does not have permission to delete this portfolio!"
        return render_template('error.html', message=message)
    else:
        db.session.delete(portfolio)
        db.session.commit()
        return redirect(url_for('view_portfolios'))