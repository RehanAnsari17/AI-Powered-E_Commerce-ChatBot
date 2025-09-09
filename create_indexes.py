from qdrant_client import QdrantClient
from config import CLUSTER_URL, QDRANT_API_KEY, COLLECTION_NAME

client = QdrantClient(url=CLUSTER_URL, api_key=QDRANT_API_KEY)

# All payload fields from your upload
indexes = [
    "id",
    "gender",
    "masterCategory",
    "subCategory",
    "articleType",
    "baseColour",
    "season",
    "year",
    "usage",
    "productDisplayName"
]

for field in indexes:
    try:
        print(f"⚙️ Creating index for {field}...")
        client.create_payload_index(
            collection_name=COLLECTION_NAME,
            field_name=field,
            field_schema="keyword"  # keyword = exact match, good for filtering
        )
        print(f"✅ Index created for {field}")
    except Exception as e:
        print(f"⚠️ Could not create index for {field}: {e}")

print("🎉 All indexes processed!")
