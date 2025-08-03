import json
import pandas as pd
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import PointStruct
from sentence_transformers import SentenceTransformer
from kaggle_secrets import UserSecretsClient

# --- Kaggle Setup ---
user_secrets = UserSecretsClient()
QDRANT_API_KEY = user_secrets.get_secret("QDRANT_API_KEY")
CLUSTER_URL = "https://c2b883ba-be1e-482f-813d-bf7d79b3cb48.europe-west3-0.gcp.cloud.qdrant.io"
COLLECTION_NAME = "my_collection"

# --- Initialize Models ---
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")  # 384-dim embeddings

# --- Load Data ---
df = pd.read_csv("/kaggle/input/dataset-qdrant/styles.csv", on_bad_lines="skip")
df.fillna("NA", inplace=True)

with open("/kaggle/input/dataset-qdrant/cloudinary_mapping.json", "r") as f:
    mapping = json.load(f)

# --- Qdrant Client ---
client = QdrantClient(url=CLUSTER_URL, api_key=QDRANT_API_KEY)

# --- Create/Recreate Collection ---
client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=models.VectorParams(
        size=384,  # Matches all-MiniLM-L6-v2
        distance=models.Distance.COSINE,
    ),
)

# --- Embedding Function ---
def get_embedding(text):
    combined_text = f"{text['productDisplayName']} {text['baseColour']} {text['masterCategory']} {text['usage']}"
    return embedding_model.encode(combined_text).tolist()

# --- Batch Upload ---
BATCH_SIZE = 100
points = []

for filename, url in mapping.items():
    try:
        product_id = int(filename.split(".")[0])
        product_data = df[df["id"] == product_id].iloc[0]
        
        payload = {
            "image_url": url,
            "productDisplayName": product_data["productDisplayName"],
            "masterCategory": product_data["masterCategory"],
            "subCategory": product_data["subCategory"],
            "articleType": product_data["articleType"],
            "baseColour": product_data["baseColour"],
            "season": product_data["season"],
            "year": str(product_data["year"]),
            "usage": product_data["usage"],
            "gender": product_data.get("gender", "Unisex"),
        }

        # Generate embedding from product metadata
        vector = get_embedding(payload)

        points.append(
            PointStruct(
                id=product_id,
                vector=vector,
                payload=payload,
            )
        )

        if len(points) >= BATCH_SIZE:
            client.upsert(collection_name=COLLECTION_NAME, points=points)
            print(f"✅ Uploaded batch of {len(points)} items")
            points = []

    except Exception as e:
        print(f"❌ Failed on {filename}: {str(e)}")

# Upload final batch
if points:
    client.upsert(collection_name=COLLECTION_NAME, points=points)
    print(f"✅ Uploaded final batch of {len(points)} items")

print("✨ All data uploaded with embeddings!")