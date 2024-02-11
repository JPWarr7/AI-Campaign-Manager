from app.database.execute import execute_query


def create_account_query(username, password):
    statement = """
		insert into users (username, password)
		values (
			%(username)s, 
			%(password)s
		)
	"""
    data = {
        "username": username,
        "password": password,
    }
    print("Account create")
    return execute_query(statement, data, action="write")


def auth_query(username):
    statement = """
		select U.usr_id
			from users as U 
			where U.username = %(username)s
	"""
    data = {"username": username}
    print("Account select")
    return execute_query(statement, data)


def register_query(username, password):
    (valid, result) = create_account_query(username, password)
    if not valid:
        return valid, result
    return auth_query(username)
