from qdrant_client import QdrantClient
from qdrant_client.models import PayloadSchemaType
from dotenv import load_dotenv
from config import CLUSTER_URL, COLLECTION_NAME, QDRANT_API_KEY
import os

# Load environment variables
load_dotenv()

# Initialize client
client = QdrantClient(
    url=CLUSTER_URL,
    api_key=QDRANT_API_KEY
)
print("Client info:", client.get_collections())  # Debug output

# Verify collection exists
try:
    collection_info = client.get_collection(COLLECTION_NAME)
    print(f"✅ Collection '{COLLECTION_NAME}' exists")
except Exception as e:
    print(f"❌ Collection '{COLLECTION_NAME}' missing. Create it first!")
    raise

# Define fields to index (MUST match EXACTLY with payload keys)
index_fields = [
    "baseColour",       # Filter by color
    "masterCategory",   # Filter by main category
    "subCategory",      # Filter by subcategory
    "articleType",      # Filter by product type
    "gender"           # Filter by gender
]

for field in index_fields:
    try:
        # Delete old index if exists
        client.delete_payload_index(
            collection_name=COLLECTION_NAME,  # Use the imported constant
            field_name=field
        )
        print(f"🗑️ Deleted old index for '{field}' (if existed)")

        # Create new keyword index
        client.create_payload_index(
            collection_name=COLLECTION_NAME,  # Use the imported constant
            field_name=field,
            field_schema=PayloadSchemaType.KEYWORD,
            wait=True
        )
        print(f"✅ Created keyword index for '{field}'")

    except Exception as e:
        print(f"❌ Failed to create index for '{field}': {str(e)}")

print("✨ All indexes created successfully!")