from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from dotenv import load_dotenv
import pandas as pd
import os
import uuid
import time
from sentence_transformers import SentenceTransformer  # ✅ New import

# Load environment variables
load_dotenv()

CLUSTER_URL = "add yours"
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "my_collection")

print("Using Qdrant URL:", CLUSTER_URL)
print("API key loaded:", bool(QDRANT_API_KEY))

# Initialize clients
client = QdrantClient(url=CLUSTER_URL, api_key=QDRANT_API_KEY, timeout=30.0)
model = SentenceTransformer('all-MiniLM-L6-v2')  # ✅ Use open-source 768-dim model

# Embedding batch generator
def get_batch_embeddings(texts):
    try:
        return model.encode(texts, show_progress_bar=False)
    except Exception as e:
        print("❌ Embedding batch failed:", e)
        return []

# Paths
image_folder = "E:\\AI-Powered ChatBot\\Trend-Setters\\static\\img"
csv_file = "E:\\AI-Powered ChatBot\\Trend-Setters\\data\\fashion\\styles.csv"

# Load CSV
df = pd.read_csv(csv_file, on_bad_lines='skip')
print(f"📄 Total records in CSV: {len(df)}")

# Normalize columns
df.columns = df.columns.str.strip().str.lower()

# Filter rows with existing images
image_set = set(os.listdir(image_folder))
df["id"] = df["id"].astype(str)
df["filename"] = df["id"] + ".jpg"
df = df[df["filename"].isin(image_set)]

print(f"🖼 Matched records with images: {len(df)}")

# Prepare embedding texts and payloads
batch_size = 96
all_payloads = []
embedding_texts = []

for idx, row in df.iterrows():
    try:
        payload = {
            "product_id": str(uuid.uuid4()),
            "name": row["productdisplayname"],
            "image_url": f"/static/img/{row['filename']}",
            "colour": row.get("basecolour", "NA"),
            "Category": row.get("mastercategory", "NA"),
            "Individual_category": row.get("subcategory", "NA"),
            "category_by_Gender": row.get("gender", "NA")
        }
        embed_text = f"{payload['colour']} {payload['Individual_category']} {payload['Category']} {payload['category_by_Gender']}"
        all_payloads.append(payload)
        embedding_texts.append(embed_text)
    except Exception as e:
        print(f"⚠️ Skipped row {idx} due to error:", e)

# Embed and upload in batches
points = []
for i in range(0, len(all_payloads), batch_size):
    payload_batch = all_payloads[i:i+batch_size]
    embed_batch = embedding_texts[i:i+batch_size]
    vectors = get_batch_embeddings(embed_batch)

    for j, vector in enumerate(vectors):
        points.append(PointStruct(
            id=i + j,
            vector=vector.tolist(),  # Convert NumPy array to list
            payload=payload_batch[j]
        ))

    print(f"🧠 Embedded batch {i//batch_size + 1}")
    time.sleep(0.3)  # Slight delay to avoid overload

# Upload to Qdrant
QDRANT_BATCH_SIZE = 20
try:
    for i in range(0, len(points), QDRANT_BATCH_SIZE):
        batch = points[i:i+QDRANT_BATCH_SIZE]
        client.upsert(collection_name=COLLECTION_NAME, points=batch)
        print(f"✅ Uploaded batch {i//QDRANT_BATCH_SIZE + 1}")
        time.sleep(0.2)

    print("🎉 All product data uploaded successfully!")

except Exception as e:
    print("❌ Upload failed:", str(e))






# from qdrant_client import QdrantClient
# from qdrant_client.models import PointStruct
# from dotenv import load_dotenv
# import os
# import uuid
# import time
# import cohere
# import random

# load_dotenv()

# CLUSTER_URL = "https://c2b883ba-be1e-482f-813d-bf7d79b3cb48.europe-west3-0.gcp.cloud.qdrant.io"
# QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
# COLLECTION_NAME = os.getenv("COLLECTION_NAME", "my_collection")
# COHERE_API_KEY = os.getenv("COHERE_API_KEY")

# print("Using Qdrant URL:", CLUSTER_URL)
# print("API key loaded:", bool(QDRANT_API_KEY))

# client = QdrantClient(
#     url=CLUSTER_URL,
#     api_key=QDRANT_API_KEY,
#     timeout=30.0
# )

# co = cohere.Client(COHERE_API_KEY)

# # Generate a real 1024-dimensional embedding using Cohere
# def get_embedding_vector(text):
#     response = co.embed(
#         texts=[text],
#         model="embed-english-v3.0",  # 1024-dim output by default
#         input_type="classification"
#     )
#     return response.embeddings[0]

# # Get all image paths
# image_folder = "E:\\AI-Powered ChatBot\\Trend-Setters\\static\\img"
# image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

# print(f"🖼 Found {len(image_files)} image files.")

# # Prepare data points
# points = []
# for idx, image_file in enumerate(image_files):
#     payload = {
#         "product_id": str(uuid.uuid4()),
#         "name": image_file,
#         "image_url": f"/static/img/{image_file}",
#         "colour": random.choice(["Black", "Red", "Blue", "Green"]),
#         "Category": random.choice(["Indian Wear", "Western"]),
#         "Individual_category": random.choice(["kurtis", "jeans", "tops", "jumpsuits"]),
#         "category_by_Gender": random.choice(["Women", "Men"]),
#     }

#     text_for_embedding = f"{payload['colour']} {payload['Individual_category']} {payload['Category']} {payload['category_by_Gender']}"
#     vector = get_embedding_vector(text_for_embedding)

#     points.append(PointStruct(
#         id=idx,
#         vector=vector,
#         payload=payload
#     ))

# # Batch upload
# BATCH_SIZE = 20
# try:
#     for i in range(0, len(points), BATCH_SIZE):
#         batch = points[i:i+BATCH_SIZE]
#         client.upsert(
#             collection_name=COLLECTION_NAME,
#             points=batch
#         )
#         print(f"✅ Uploaded batch {i//BATCH_SIZE + 1}")
#         time.sleep(0.5)

#     print("🎉 All product data uploaded successfully!")

# except Exception as e:
#     print("❌ Error during upload:", str(e))



# from qdrant_client import QdrantClient
# from qdrant_client.models import PointStruct
# from dotenv import load_dotenv
# import os
# import uuid
# import random
# import time

# # Load environment variables
# load_dotenv()

# CLUSTER_URL = "https://c2b883ba-be1e-482f-813d-bf7d79b3cb48.europe-west3-0.gcp.cloud.qdrant.io"
# QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
# COLLECTION_NAME = os.getenv("COLLECTION_NAME", "my_collection")

# print("Using Qdrant URL:", CLUSTER_URL)
# print("API key loaded:", bool(QDRANT_API_KEY))

# # Initialize Qdrant client
# client = QdrantClient(
#     url=CLUSTER_URL,
#     api_key=QDRANT_API_KEY,
#     timeout=30.0
# )

# # Simulate a 768-dimension dummy vector
# vector = [random.random() for _ in range(768)]

# # Add the specific product (black kurti for women)
# product = {
#     "product_id": str(uuid.uuid4()),
#     "name": "black_kurti.jpg",
#     "image_url": f"/static/img/sample_image.jpg",
#     "colour": "Black",
#     "Category": "Indian Wear",
#     "Individual_category": "kurti",
#     "category_by_Gender": "Women"
# }

# point = PointStruct(
#     id=0,
#     vector=vector,
#     payload=product
# )

# try:
#     client.upsert(
#         collection_name=COLLECTION_NAME,
#         points=[point]
#     )
#     print("✅ Black kurti uploaded successfully!")
# except Exception as e:
#     print("❌ Upload failed:", str(e))




# from qdrant_client import QdrantClient
# from qdrant_client.models import PointStruct, Distance, VectorParams
# from dotenv import load_dotenv
# import os
# import uuid
# import random
# import time
# from PIL import Image
# import numpy as np

# load_dotenv()

# CLUSTER_URL = "https://c2b883ba-be1e-482f-813d-bf7d79b3cb48.europe-west3-0.gcp.cloud.qdrant.io"
# QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
# COLLECTION_NAME = os.getenv("COLLECTION_NAME", "my_collection")

# print("Using Qdrant URL:", CLUSTER_URL)
# print("API key loaded:", bool(QDRANT_API_KEY))

# client = QdrantClient(
#     url=CLUSTER_URL,
#     api_key=QDRANT_API_KEY,
#     timeout=30.0  # seconds
# )

# # Simulate dummy vector for now
# def get_dummy_vector():
#     return [random.random() for _ in range(768)]

# # Get all image paths
# image_folder = "E:\\AI-Powered ChatBot\\Trend-Setters\\static\\img"
# image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

# print(f"🖼 Found {len(image_files)} image files.")

# # Prepare data points
# points = []
# for idx, image_file in enumerate(image_files):
#     payload = {
#         "product_id": str(uuid.uuid4()),
#         "name": image_file,
#         "image_url": f"/static/img/{image_file}",
#         "colour": random.choice(["Black", "Red", "Blue", "Green"]),
#         "Category": random.choice(["Indian Wear", "Western"]),
#         "Individual_category": random.choice(["kurtis", "jeans", "tops"]),
#         "category_by_Gender": random.choice(["Women", "Men"]),
#     }

#     points.append(PointStruct(
#         id=idx,
#         vector=get_dummy_vector(),
#         payload=payload
#     ))

# # Batch upload
# BATCH_SIZE = 20
# try:
#     for i in range(0, len(points), BATCH_SIZE):
#         batch = points[i:i+BATCH_SIZE]
#         client.upsert(
#             collection_name=COLLECTION_NAME,
#             points=batch
#         )
#         print(f"✅ Uploaded batch {i//BATCH_SIZE + 1}")
#         time.sleep(0.5)  # optional: add short delay to be safe

#     print("🎉 All product data uploaded successfully!")

# except Exception as e:
#     print("❌ Error during upload:", str(e))
