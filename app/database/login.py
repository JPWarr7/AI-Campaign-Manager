from .execute import execute_query

def account_query(usr_id):
    statement = """
		select U.usr_id, U.username
			from users as U
			where U.usr_id = %(usr_id)s
	"""
    data = {"usr_id": usr_id}
    return execute_query(statement, data)


def username_query(username):
    statement = """
		select U.usr_id 
			from users as U 
			where U.username = %(username)s
	"""
    data = {"username": username}
    return execute_query(statement, data)


def password_query(user_id, password):
    statement = """
		select U.usr_id 
			from users as U 
			where 	
				U.usr_id = %(user_id)s and 
				U.password = %(password)s;
	"""
    data = {"user_id": user_id, "password": password}
    return execute_query(statement, data)


def login_query(username, password):
    (valid, result) = username_query(username)
    if not valid:
        return False, {"username": f"No account with username {username}!"}
    user_id = result["usr_id"]
    valid, result = password_query(user_id, password)
    if not valid:
        return False, {"password": f"Incorrect password!"}
    return valid, result
