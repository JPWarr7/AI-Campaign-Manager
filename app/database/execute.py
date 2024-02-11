from app import mysql, init_cursor

actions = {"read", "write"}


def execute_query(statement: str, data: dict | list[dict] = None, action="read", many=False):
    """
	Executes an SQL query with specified parameters

	Parameters:
	- `statement (str)`: The SQL query to execute
	- `data (dict | list)`: The parameters needed for the query
	- `action? (str)`: Must be one of the following
		- `"read"`: To read from the database
		- `"write"`: To write from the database 
		- Defaults to `"read"`
	- `many? (bool)`: 
		- Operates on multiple rows if `True`
		- Otherwise assumes one row
		- Defaults to `False`
	"""
    if data is None:
        data = {}
    if action not in actions:
        valid_actions = ",".join(actions)
        raise ValueError(f"Invalid action \"{action}\"\nValid actions are: {valid_actions}")
    if action == "write":
        if isinstance(data, list) and not many:
            raise TypeError(
                f"Invalid arguments:\nmany=False specified for bulk write query")
        if isinstance(data, dict) and many:
            raise TypeError(
                f"Invalid arguments:\nmany=True specified for single-row write query")

    cursor = init_cursor()
    clean_statement = statement.strip()
    if action == "read":
        cursor.execute(clean_statement, data)
        result = (cursor.fetchall() or []) if many else cursor.fetchone()
        return result is not None, result

    if many:
        result = cursor.executemany(clean_statement, data)
    else:
        result = cursor.execute(clean_statement, data)
    mysql.connection.commit()
    return True, result
