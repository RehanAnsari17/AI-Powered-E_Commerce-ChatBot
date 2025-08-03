import json
import cloudinary
import cloudinary.uploader
import os
import pandas as pd
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

# Path to styles.csv (contains metadata)
styles_path = "E:\\AI-Powered ChatBot\\E-Commerce_ChatBot\\data\\fashion\\styles.csv"

# Read CSV safely (skip bad lines to avoid ParserError)
styles_df = pd.read_csv(styles_path, on_bad_lines='skip', engine='python')

# Build dictionary for quick lookup: id.jpg → metadata
metadata_lookup = {}
for _, row in styles_df.iterrows():
    filename = str(row['id']) + ".jpg"
    metadata_lookup[filename] = {
        "gender": str(row.get('gender', '')),
        "masterCategory": str(row.get('masterCategory', '')),
        "subCategory": str(row.get('subCategory', '')),
        "articleType": str(row.get('articleType', '')),
        "baseColour": str(row.get('baseColour', '')),
        "season": str(row.get('season', '')),
        "year": str(row.get('year', '')),
        "usage": str(row.get('usage', '')),
        "productDisplayName": str(row.get('productDisplayName', ''))
    }

# Folder containing images
folder = "E:\\AI-Powered ChatBot\\E-Commerce_ChatBot\\static\\img"

# Upload images with metadata
mapping = {}  # filename → cloudinary_url mapping

for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    if os.path.isfile(file_path):
        try:
            # Attach metadata if available
            context = metadata_lookup.get(filename, {})
            response = cloudinary.uploader.upload(
                file_path,
                folder="fashion-images",
                context=context  # metadata added here
            )
            url = response['secure_url']
            mapping[filename] = url
            print(f"Uploaded {filename}: {url} with metadata {context}")
        except Exception as e:
            print(f"❌ Failed to upload {filename}: {e}")

# Save mapping to JSON
with open("cloudinary_mapping.json", "w") as f:
    json.dump(mapping, f)

print("Mapping saved to cloudinary_mapping.json")