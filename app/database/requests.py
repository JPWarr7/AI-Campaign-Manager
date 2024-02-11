from app.database.execute import execute_query
from app.routes.utils.normalize import normalize


def view_requests_broker(bkr_id):
	statement = """
		call view_requests(null, %(bkr_id)s, null, null);
	"""
	data = {"bkr_id": bkr_id}
	return execute_query(statement, data, many=True)


def view_requests_trader(tdr_id):
	statement = """
		call view_requests(%(tdr_id)s, null, null, null);
	"""
	data = {"tdr_id": tdr_id}
	return execute_query(statement, data, many=True)


def view_pending_requests_trader(tdr_id):
	statement = """
		call view_requests(%(tdr_id)s, null, null, 1);
	"""
	data = {"tdr_id": tdr_id}
	return execute_query(statement, data, many=True)


def view_pending_requests_broker(bkr_id):
	statement = """
		call view_requests(null, %(bkr_id)s, null, 1);
	"""
	data = {"bkr_id": bkr_id}
	return execute_query(statement, data, many=True)


def request_max(req_id):
	statement = """
		select max_fill_shares(%(req_id)s) as value
	"""
	data = {"req_id": req_id}
	return execute_query(statement, data)


def create_request(usr_id, bkr_id, stk_id, amount, exchange_type):
	statement = """
		call create_request(%(usr_id)s, %(stk_id)s, %(bkr_id)s, %(amount)s, %(exchange_type)s);
	"""
	data = {
		"usr_id": usr_id, 
		"stk_id": stk_id,
		"bkr_id": bkr_id,
		"amount": normalize(amount),
		"exchange_type": exchange_type
	}
	return execute_query(statement, data, action="write")


def buy_query(usr_id, bkr_id, stk_id, amount):
	return create_request(usr_id, bkr_id, stk_id, amount, exchange_type="Buy")


def sell_query(usr_id, bkr_id, stk_id, amount):
	return create_request(usr_id, bkr_id, stk_id, amount, exchange_type="Sell")


def approve_request_query(req_id, final_amount):
	statement = """
		call approve_request(%(req_id)s, %(final_amount)s);
	"""
	data = {
		"req_id": req_id,
		"final_amount": final_amount
	}
	return execute_query(statement, data, action="write")


def deny_request_query(req_id):
	statement = """
		call deny_request(%(req_id)s)
	"""
	data = {"req_id": req_id}
	return execute_query(statement, data, action="write")
