from flask import redirect, render_template, request, url_for, flash
from app import app
from app.database import profile_query, stock_broker_query, stock_info_query
from app.database.shares import unowned_share_count, total_share_count, create_shares, delete_shares, num_shares_owned
from app.database.stocks import create_stock, stocks_query, stock_history, delist_stock
from app.database.requests import buy_query, sell_query
from app.forms import AddSharesForm, RemoveSharesForm, DelistStockForm
from app.forms.request import CreateBuyRequestForm, CreateSellRequestForm, HandleRequestForm
from app.forms.stock import StockForm
from app.routes.profile import profile_set
from app.routes.utils import is_trader, is_broker, login_required


@app.route("/stock/<usr_id>", methods=["GET", "POST"])
@login_required
@profile_set
def view_all_stocks(usr_id):
    stock_form = StockForm(values=request.form)
    _, stocks = stocks_query()
    _, profile = profile_query(usr_id)
    if request.method == "POST":
        if stock_form.is_valid():
            return redirect(url_for('add_stock'))
        stock_form.before_render()
    else:
        stock_form.clear()
    template = f"./pages/view_stocks.html"
    return render_template(template, usr_id=usr_id, stocks=stocks, profile=profile, stock_form=stock_form)


def stock_data(stk_id: int, bkr_id: int = None, tdr_id: int = None):
    _, brokers = stock_broker_query(stk_id)
    _, requests = stock_history(stk_id)
    _, unowned_count = unowned_share_count(stk_id)
    _, owned_count = num_shares_owned(stk_id, bkr_id=bkr_id, tdr_id=tdr_id)
    if not owned_count:
        owned_count = {"owned": 0}
    _, total_count = total_share_count(stk_id)
    return {
        "brokers": brokers,
        "requests": requests,
        "num_shares": {
            **owned_count,
            **unowned_count,
            **total_count
        }
    }


@app.route("/stock/trader/<usr_id>/<stk_id>", methods=["GET", "POST"])
@login_required
@profile_set
@is_trader
def view_stock_trader(usr_id, stk_id, error=None):
    valid, stock = stock_info_query(stk_id)
    if not valid:
        return render_template("404.html")
    stk_data = stock_data(stk_id, tdr_id=usr_id)

    stk_name = stock['name']
    buy_form = CreateBuyRequestForm(stk_id=stk_id, stk_name=stk_name)
    print(buy_form.amount.max)
    sell_form = None
    if stk_data["num_shares"]["owned"] > 0:
        sell_form = CreateSellRequestForm(stk_id=stk_id, tdr_id=usr_id, stk_name=stk_name)
    print(buy_form.amount.max)

    # something post
    if error:
        flash("error", "error")

    template = "./pages/trader/view_stock.html"
    return render_template(template, usr_id=usr_id, stk_id=stk_id, stock=stock, **stk_data,
                           buy_form=buy_form, sell_form=sell_form)


@app.route("/stock/broker/<usr_id>/<stk_id>", methods=["GET", "POST"])
@login_required
@profile_set
@is_broker
def view_stock_broker(usr_id, stk_id):
    valid, stock = stock_info_query(stk_id)
    if not valid:
        return render_template("404.html")
    stk_data = stock_data(stk_id, bkr_id=usr_id)

    forms = {
        "add_shares_form": AddSharesForm(),
        "remove_shares_form": RemoveSharesForm(),
        "delist_stock_form": DelistStockForm()
    }

    def append_request_form(row):
        if row["final_amount"] is None:
            row["form"] = HandleRequestForm(req_id=row["req_id"], stk_id=stk_id)
        return row

    stk_data["requests"] = list(map(append_request_form, stk_data["requests"]))
    template = "./pages/broker/view_stock.html"
    return render_template(template, usr_id=usr_id, stk_id=stk_id, stock=stock, **stk_data, **forms)


@app.route("/stock/<usr_id>/add", methods=["POST"])
@login_required
@profile_set
@is_broker
def add_stock(usr_id):
    _, result = create_stock(bkr_id=usr_id, **request.form)
    return redirect(url_for("view_all_stocks", usr_id=usr_id))


@app.route("/stock/<stk_id>/remove/<usr_id>", methods=["POST"])
@login_required
@profile_set
@is_broker
def remove_stock(stk_id, usr_id):
    _, stock = stock_info_query(stk_id)
    stk_code = stock["code"]
    stk_name = stock["name"]
    _, result = delist_stock(stk_id)
    if result:
        flash(f"{stk_name} ({stk_code}) has been de-listed", "error")
    return redirect(url_for("view_all_stocks", usr_id=usr_id, stk_id=stk_id))


@app.route("/stock/buy/<stk_id>/<usr_id>", methods=["POST"])
@login_required
@profile_set
@is_trader
def buy_stock(stk_id, usr_id):
    _, stock = stock_info_query(stk_id)
    buy_form = CreateBuyRequestForm(stk_id=stk_id, values=request.form)
    if not buy_form.is_valid():
        error = buy_form.errors.values()
        return redirect(url_for("view_stock_trader", usr_id=usr_id, stk_id=stk_id, error=error))
    _, result = buy_query(stk_id=stk_id, usr_id=usr_id, **request.form)
    return redirect(url_for("view_stock_trader", usr_id=usr_id, stk_id=stk_id))


@app.route("/stock/<stk_id>/sell/<usr_id>", methods=["POST"])
@login_required
@profile_set
@is_trader
def sell_stock(stk_id, usr_id):
    print(request.form)
    sell_form = CreateSellRequestForm(stk_id=stk_id, tdr_id=usr_id, values=request.form)
    if not sell_form.is_valid():
        error = sell_form.errors.values()
        return redirect(url_for("view_stock_trader", usr_id=usr_id, stk_id=stk_id, error=error))
    _, result = sell_query(stk_id=stk_id, usr_id=usr_id, **request.form)
    return redirect(url_for("view_stock_trader", usr_id=usr_id, stk_id=stk_id))


@app.route("/shares/add/<usr_id>/<stk_id>", methods=["POST"])
@login_required
@profile_set
@is_broker
def add_shares(usr_id, stk_id):
    print(f"DATA {request.form}")
    _, result = create_shares(stk_id=stk_id, bkr_id=usr_id, **request.form)
    flash("Shares Added", "success")
    return redirect(url_for("view_stock_broker", usr_id=usr_id, stk_id=stk_id))


@app.route("/shares/remove/<usr_id>/<stk_id>", methods=["POST"])
@login_required
@profile_set
@is_broker
def remove_shares(usr_id, stk_id):
    print(f"DATA {request.form}")
    _, result = delete_shares(stk_id=stk_id, bkr_id=usr_id, **request.form)
    flash("Shares Removed", "success")
    return redirect(url_for("view_stock_broker", usr_id=usr_id, stk_id=stk_id))
