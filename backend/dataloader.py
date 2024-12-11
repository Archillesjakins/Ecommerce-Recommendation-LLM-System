from llama_index.readers.database import DatabaseReader
import pymysql
MySQLdb = pymysql.install_as_MySQLdb()

# Define your SQL query for user interactions
query = "SELECT user_id, item_id, swipe_action, metadata FROM user_interactions;"


# Initialize DatabaseReader with the SQL database connection details
reader = DatabaseReader(
    sql_database=None,  
    engine=None,  
    scheme="mysql",  
    host="127.0.0.1",  
    port="3306",  
    user="root",  
    password="Archilles5522",  
    dbname="User",  
)

# Load data from the database using a query

def dataload():
    user_data = reader.load_data(
    query=query 
    )
    user_data = [
    doc.to_embedchain_format()
    for doc in user_data
    ]
    return user_data
