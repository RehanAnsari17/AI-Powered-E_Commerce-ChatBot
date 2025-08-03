from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

CLUSTER_URL = "add yours"
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "my_collection")

# Initialize client
client = QdrantClient(
    url=CLUSTER_URL,
    api_key=QDRANT_API_KEY,
    timeout=30.0
)

# Delete old collection if exists
if client.collection_exists(COLLECTION_NAME):
    client.delete_collection(COLLECTION_NAME)
    print(f"🗑️ Deleted existing collection: {COLLECTION_NAME}")

# Create new collection with 384-dimensional vectors
client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)

print(f"✅ Collection '{COLLECTION_NAME}' created with vector size 384.")




# from qdrant_client import QdrantClient
# from qdrant_client.models import VectorParams, Distance
# from dotenv import load_dotenv
# import os

# load_dotenv()

# CLUSTER_URL = "https://c2b883ba-be1e-482f-813d-bf7d79b3cb48.europe-west3-0.gcp.cloud.qdrant.io"
# QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
# COLLECTION_NAME = os.getenv("COLLECTION_NAME", "my_collection")

# client = QdrantClient(
#     url=CLUSTER_URL,
#     api_key=QDRANT_API_KEY,
#     timeout=30.0
# )

# # Delete old collection if it exists
# if client.collection_exists(COLLECTION_NAME):
#     client.delete_collection(COLLECTION_NAME)
#     print(f"🗑️ Deleted existing collection: {COLLECTION_NAME}")

# # Create new collection with 1024-dimensional vectors
# client.recreate_collection(
#     collection_name=COLLECTION_NAME,
#     vectors_config=VectorParams(size=1024, distance=Distance.COSINE)
# )

# print(f"✅ Collection '{COLLECTION_NAME}' created with vector size 1024.")
