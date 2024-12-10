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
    query=query # SQL query parameter to filter tables and rows
    )
    user_data = [
    doc.to_embedchain_format()
    for doc in user_data
    ]
    return user_data


def transform_data_for_google_gemini(loader_output):
    """
    Transform the data loader output to match the expected format of Google Gemini API.
    """
    transformed_data = []
    
    for entry in loader_output:
        content = entry['data'].get('content', '')  # Extract content
        transformed_data.append({
            "parts": [
                {"text": content}  # Wrap content in the 'parts' format
            ]
        })
    
    return transformed_data

transformed_data = transform_data_for_google_gemini(dataload())
user_data = str(transformed_data)

# print(user_data)