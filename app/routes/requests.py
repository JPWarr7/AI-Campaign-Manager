from flask import render_template, request, redirect, url_for
from app import app
from app.database import profile_query, view_requests_trader, view_requests_broker, approve_request_query, deny_request_query
from app.routes.profile import profile_set
from app.routes.utils import login_required
from app.forms.request import HandleRequestForm


def add_handle_form(requests):
    new_requests = []
    for r in requests:
        if r["final_amount"] is None:
            r["form"] = HandleRequestForm(r["req_id"], r["stk_id"])
        new_requests.append(r)
    return new_requests


@app.route("/requests/trader/<usr_id>", methods=["GET"])
@login_required
@profile_set
def view_all_requests_trader(usr_id):
    _, requests = view_requests_trader(tdr_id=usr_id)
    requests = add_handle_form(requests)
    _, profile = profile_query(usr_id)
    template = f"./pages/view_requests.html"
    return render_template(template, usr_id=usr_id, requests=requests, profile=profile)


@app.route("/requests/broker/<usr_id>", methods=["GET"])
@login_required
@profile_set
def view_all_requests_broker(usr_id):
    _, requests = view_requests_broker(bkr_id=usr_id)
    requests = add_handle_form(requests)
    _, profile = profile_query(usr_id)
    template = f"./pages/view_requests.html"
    return render_template(template, usr_id=usr_id, requests=requests, profile=profile)


@app.route("/requests/<req_id>/approve/<stk_id>/<usr_id>", methods=["POST"])
@login_required
@profile_set
def approve_request(req_id, stk_id, usr_id):
    final_amount = request.form["amount"] or 0
    if final_amount == 0:
        redirect(url_for("deny_request", req_id=req_id, stk_id=stk_id, usr_id=usr_id))
    _, result = approve_request_query(req_id, final_amount)
    return redirect(url_for("view_stock_broker", stk_id=stk_id, usr_id=usr_id))


@app.route("/requests/<req_id>/deny/<stk_id>/<usr_id>", methods=["GET"])
def deny_request(req_id, stk_id, usr_id):
    deny_request_query(req_id)
    return redirect(url_for("view_stock_broker", stk_id=stk_id, usr_id=usr_id))
