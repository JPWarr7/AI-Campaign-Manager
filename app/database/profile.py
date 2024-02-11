from app.database.execute import execute_query


def profile_query(usr_id):
    statement = """
		select U.first_name, U.last_name, U.account_type
			from users as U
			where U.usr_id = %(usr_id)s
	"""
    data = {"usr_id": usr_id}
    return execute_query(statement, data)


def update_profile_query(usr_id, first_name, last_name, account_type):
    statement = """
		update users
			set first_name = %(first_name)s, 
			last_name = %(last_name)s, 
			account_type = %(account_type)s
		where usr_id = %(usr_id)s
	"""
    data = {
        "usr_id": usr_id,
        "first_name": first_name,
        "last_name": last_name,
        "account_type": account_type
    }
    return execute_query(statement, data, action="write")
