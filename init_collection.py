from qdrant_client import QdrantClient
from qdrant_client.http import models as rest
from config import CLUSTER_URL, QDRANT_API_KEY, COLLECTION_NAME

# Example: Assuming vector size 768 (change if needed)
VECTOR_SIZE = 768

client = QdrantClient(url=CLUSTER_URL, api_key=QDRANT_API_KEY)

# Create or recreate the collection
client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=rest.VectorParams(size=VECTOR_SIZE, distance=rest.Distance.COSINE)
)

print("✅ Collection created or reset successfully!")