from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.gemini import GeminiEmbedding
from openai import OpenAI
import google.generativeai as genai
import numpy as np
from dotenv import dotenv_values
from dataloader import user_data

config = dotenv_values(".env")

# Initialize embedding models conditionally based on API key availability
def initialize_embedder():
    EMBEDDING_MODELS = {
    'openai': {
        'model': "text-embedding-3-small",
        'api_key': config.get('openai_api_key')
    },
    'gemini': {
        'model': "models/embedding-001",
        'api_key': config.get('api_keys')
    }
}

EMBEDDING_MODELS = initialize_embedder()    
# Function to generate embeddings based on available models
def generate_embeddings(text, embedding_type='gemini'):

    if embedding_type == 'openai':
                client = OpenAI(api_key=EMBEDDING_MODELS['openai']['api_key'])
                response = client.embeddings.create(
                    input=text,
                    model=EMBEDDING_MODELS['openai']['model']
                )
                embeddings = response.data[0].embedding
            
    elif embedding_type == 'gemini':
            genai.configure(api_key=EMBEDDING_MODELS['gemini']['api_key'])
            embedding_model = genai.embedding_models()[EMBEDDING_MODELS['gemini']['model']]
            embeddings = embedding_model.embed(text).embedding
            
    else:
        raise ValueError(f"Unsupported embedding type: {embedding_type}")

    return embeddings
   
# Generate embeddings for item data
item_embeddings = generate_embeddings(user_data)
print(item_embeddings)




from sqlalchemy import create_engine
from llama_index.readers.database import DatabaseReader

# Define SQLAlchemy engine
engine = create_engine("mysql+pymysql://root:Archilles5522@127.0.0.1:3306/fashion_app_db")

# Pass the engine to DatabaseReader
reader = DatabaseReader(
    sql_database=None,
    engine=engine,
)




# # Define a SQL query
# query2 = "SELECT item_id FROM user_interactions WHERE user_id = 2;"

# # Use the reader to execute the query
# user_interactions = reader.load_data(query2)

# # Output: [{'item_id': 101, 'swipe_action': 'like'}, {'item_id': 102, 'swipe_action': 'dislike'}, ...]
# print(user_interactions)
