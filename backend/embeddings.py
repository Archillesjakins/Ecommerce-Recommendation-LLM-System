# from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.gemini import GeminiEmbedding
from dotenv import load_dotenv
from dataloader import user_data
import os

load_dotenv()

api_keys = os.getenv('api_keys')
model_name = "models/embedding-001"

async def generate_embeddings(data):
    embed_model = GeminiEmbedding(
    model_name=model_name, api_key=api_keys, title="Database Embeddings"
    )
    embeddings = await embed_model.aget_text_embedding_batch([data])
    return embeddings([0][:5])


# Generate embeddings for item data
item_embeddings = generate_embeddings(user_data)
print(item_embeddings)
