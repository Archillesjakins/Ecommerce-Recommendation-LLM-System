from openai import OpenAI
from dotenv import load_dotenv
import os
import re
from typing import List, Dict

load_dotenv()

api_keys = os.getenv('api_keys')

def generate_embeddings(data: List[Dict]) -> Dict[int, List[float]]:
    client = OpenAI(
    api_key=api_keys,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    embeddings = {}
    
    for record in data:
        # Extract content string
        content = record['data'].get('content', '')
        
        # Parse item_id and metadata from content
        match = re.search(r'item_id: (\d+),.*metadata: ({.*})', content)
        if match:
            item_id = int(match.group(1))  # Extract item_id
            metadata = match.group(2)     # Extract metadata
            
            # Generate embedding for metadata
            embedding = client.embeddings.create(
            input=metadata,
            model="text-embedding-004"
            )
            # embeddings = embeddings.data[0].embedding
            # Store embedding with item_id as the key
            embeddings[item_id] = embedding
        else:
            print(f"Failed to parse record: {content}")
    
    return embeddings

    



