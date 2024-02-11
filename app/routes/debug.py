from app import app
from app.database import read_sql


@app.route("/init")
def init_tables():
    read_sql("drop_tables")
    read_sql("create_tables")
    read_sql("create_procedures")
    read_sql("create_triggers")
    read_sql("insert_data")
    return "Database Initialized"
