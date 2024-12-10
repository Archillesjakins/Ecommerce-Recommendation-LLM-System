import redis
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from embeddings import generate_embeddings, item_embeddings
from dataloader import reader
import pymysql
MySQLdb = pymysql.install_as_MySQLdb()




# Connect to Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)
try:
    redis_client.ping()
    print("Redis connection successful!")
except redis.ConnectionError as e:
    print(f"Redis connection failed: {e}")

# Store embeddings in Redis
for item_id, embedding in item_embeddings.items():
    redis_client.set(item_id, np.array(embedding).tobytes())

# Retrieve an embedding
def get_embedding(item_id):
    """
    Retrieve an embedding from Redis and convert it back to a NumPy array.
    """
    embedding_bytes = redis_client.get(item_id)
    if embedding_bytes is not None:
        return np.frombuffer(embedding_bytes, dtype=np.float32)
    else:
        print(f"Embedding for item_id {item_id} not found in Redis.")
        return None

def generate_user_preference_embedding(user_id, reader):
    """
    Generate the user's preference embedding based on likes and dislikes.
    """
    # Fetch user interactions from the database
    query = f"SELECT item_id, swipe_action FROM user_interactions WHERE user_id = '{user_id}';"
    user_interactions = reader.execute_query(query)
    
    liked_embeddings = []
    disliked_embeddings = []
    
    for interaction in user_interactions:
        item_id = interaction['item_id']
        swipe_action = interaction['swipe_action']
        item_embedding = get_embedding(item_id)
        
        if swipe_action == "like":
            liked_embeddings.append(item_embedding)
        elif swipe_action == "dislike":
            disliked_embeddings.append(item_embedding)
    
    # Calculate the user embedding
    if liked_embeddings:
        avg_liked = np.mean(liked_embeddings, axis=0)
    else:
        avg_liked = np.zeros(len(liked_embeddings[0]) if liked_embeddings else 512)  # Assuming embeddings are 512-dimensional
    
    if disliked_embeddings:
        avg_disliked = np.mean(disliked_embeddings, axis=0)
    else:
        avg_disliked = np.zeros(len(disliked_embeddings[0]) if disliked_embeddings else 512)
    
    # User embedding as a weighted combination
    user_embedding = avg_liked - 0.5 * avg_disliked
    return user_embedding



def update_user_embedding(user_id, new_interaction):
    # Generate new embedding
    new_embedding = generate_embeddings([new_interaction])[new_interaction['item_id']]
    
    # Update Redis and user profile
    redis_client.set(new_interaction['item_id'], new_embedding.tobytes())
    # Optionally update user profile in MySQL


# Retrieve embeddings for user preferences
user_embedding = generate_user_preference_embedding(user_id=1, reader=reader)
print(user_embedding)
# Compare with all items
recommendations = []
for item_id in redis_client.keys():
    item_embedding = get_embedding(item_id)
    similarity = cosine_similarity([user_embedding], [item_embedding])
    recommendations.append((item_id, similarity[0][0]))

# Sort by similarity score
recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)

# print(recommendations)
