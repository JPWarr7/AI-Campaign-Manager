from flask import render_template, flash
from app import app
from app.database import profile_query
from app.database.stocks import broker_stocks, trader_stocks
from app.database.requests import view_pending_requests_trader, view_pending_requests_broker
from app.routes.profile import profile_set
from app.routes.utils import login_required


@app.route("/home/<usr_id>", methods=["GET", "POST"])
@login_required
@profile_set
def home(usr_id):
	_, profile = profile_query(usr_id)
	account_type: str = profile["account_type"]
	template = f"/pages/{account_type.lower()}/home.html"
	if account_type == "Trader":  # Trader homepage
		_, stocks = trader_stocks(usr_id)
		_, requests = view_pending_requests_trader(usr_id)
	else:
		_, stocks = broker_stocks(usr_id)
		_, requests = view_pending_requests_broker(usr_id)
	data = []  # Pending requests
	return render_template(
		template, usr_id=usr_id, profile=profile,
		stocks=stocks, requests=requests, data=data)
