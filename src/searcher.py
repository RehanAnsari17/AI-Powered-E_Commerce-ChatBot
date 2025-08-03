from qdrant_client import QdrantClient
from config import CLUSTER_URL, COLLECTION_NAME, QDRANT_API_KEY
from qdrant_client.models import Filter, FieldCondition, MatchValue
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import os

# Load environment variables
load_dotenv()

# Initialize Qdrant client
client = QdrantClient(
    url=CLUSTER_URL,
    api_key=QDRANT_API_KEY
)

# Initialize SentenceTransformer model (384-dim)
model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embedding(query_text):
    return model.encode(query_text).tolist()  # Ensure it's a plain list

def search_collection(query_text="", colour="NA", individual_category="NA", category="NA", category_by_gender="NA"):
    print(f"\n📥 Incoming Filters - Colour: {colour}, Category: {category}, Individual: {individual_category}, Gender: {category_by_gender}")
    
    try:
        query_vector = generate_embedding(query_text)
        print("📡 SentenceTransformer embedding generated.")
    except Exception as e:
        print("❌ Error generating embedding:", str(e))
        return []

    # -------- Build metadata filter --------
        # -------- Build metadata filter only for non-"NA" values --------
    filter_keys = {
        "colour": colour,
        "Individual_category": individual_category,
        "Category": category,
        "category_by_Gender": category_by_gender
    }

    conditions = [
        FieldCondition(key=k, match=MatchValue(value=v))
        for k, v in filter_keys.items() if v != "NA"
    ]

    metadata_filter = Filter(must=conditions) if conditions else None

    # conditions = []
    # if colour != "NA":
    #     conditions.append(FieldCondition(key="colour", match=MatchValue(value=colour)))
    # if individual_category != "NA":
    #     conditions.append(FieldCondition(key="Individual_category", match=MatchValue(value=individual_category)))
    # if category != "NA":
    #     conditions.append(FieldCondition(key="Category", match=MatchValue(value=category)))
    # if category_by_gender != "NA":
    #     conditions.append(FieldCondition(key="category_by_Gender", match=MatchValue(value=category_by_gender)))

    # metadata_filter = Filter(must=conditions) if conditions else None

    # -------- Hybrid search (vector + filters) --------
    try:
        search_result = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            limit=10,
            query_filter=metadata_filter
        )

        if search_result:
            print(f"🛍️ Products Found: {len(search_result)}")
            return [point.payload for point in search_result]
        else:
            print("⚠️ No matching products found with filters. Trying fallback (vector-only)...")

            fallback_result = client.search(
                collection_name=COLLECTION_NAME,
                query_vector=query_vector,
                limit=10
            )
            print(f"🔁 Fallback results: {len(fallback_result)}")
            return [point.payload for point in fallback_result]

    except Exception as e:
        print("❌ Qdrant search failed:", str(e))
        return []








# from qdrant_client import QdrantClient
# from config import CLUSTER_URL, COLLECTION_NAME, QDRANT_API_KEY
# from qdrant_client.models import Filter, FieldCondition, MatchValue
# from dotenv import load_dotenv
# import os
# import cohere

# # Load environment variables
# load_dotenv()

# COHERE_API_KEY = os.getenv("COHERE_API_KEY")

# # Initialize Qdrant client
# client = QdrantClient(
#     url=CLUSTER_URL,
#     api_key=QDRANT_API_KEY
# )

# # Initialize Cohere client
# co = cohere.Client(COHERE_API_KEY)

# def generate_embedding(query_text):
#     response = co.embed(
#         texts=[query_text],
#         model="embed-english-v3.0",  # Default 1024-dim
#         input_type="search_query"
#     )
#     return response.embeddings[0]

# def search_collection(query_text="", colour="NA", individual_category="NA", category="NA", category_by_gender="NA"):
#     print(f"\n📥 Incoming Filters - Colour: {colour}, Category: {category}, Individual: {individual_category}, Gender: {category_by_gender}")
    
#     try:
#         query_vector = generate_embedding(query_text)
#         print("📡 Cohere embedding generated.")
#     except Exception as e:
#         print("❌ Error generating embedding:", str(e))
#         return []

#     # -------- Build metadata filter --------
#     conditions = []
#     if colour != "NA":
#         conditions.append(FieldCondition(key="colour", match=MatchValue(value=colour)))
#     if individual_category != "NA":
#         conditions.append(FieldCondition(key="Individual_category", match=MatchValue(value=individual_category)))
#     if category != "NA":
#         conditions.append(FieldCondition(key="Category", match=MatchValue(value=category)))
#     if category_by_gender != "NA":
#         conditions.append(FieldCondition(key="category_by_Gender", match=MatchValue(value=category_by_gender)))

#     metadata_filter = Filter(must=conditions) if conditions else None

#     # -------- Hybrid search (vector + filters) --------
#     try:
#         search_result = client.search(
#             collection_name=COLLECTION_NAME,
#             query_vector=query_vector,
#             limit=10,
#             query_filter=metadata_filter
#         )

#         if search_result:
#             print(f"🛍️ Products Found: {len(search_result)}")
#             return [point.payload for point in search_result]
#         else:
#             print("⚠️ No matching products found with filters. Trying fallback (vector-only)...")

#             # Fallback: use vector search without any metadata filters
#             fallback_result = client.search(
#                 collection_name=COLLECTION_NAME,
#                 query_vector=query_vector,
#                 limit=10
#             )
#             print(f"🔁 Fallback results: {len(fallback_result)}")
#             return [point.payload for point in fallback_result]

#     except Exception as e:
#         print("❌ Qdrant search failed:", str(e))
#         return []








# from config import CLUSTER_URL, COLLECTION_NAME, QDRANT_API_KEY
# from qdrant_client import QdrantClient
# import random

# # Initialize the Qdrant client
# client = QdrantClient(
#     url=CLUSTER_URL,
#     api_key=QDRANT_API_KEY
# )

# def search_collection(colour="NA", individual_category="NA", category="NA", category_by_gender="NA"):

#     # Debug: log received filters
#     print(f"\n📥 Incoming Filters - Colour: {colour}, Category: {category}, Individual: {individual_category}, Gender: {category_by_gender}")

#     filters = []

#     if colour != "NA":
#         filters.append(lambda point: point.payload.get("colour", "").lower() == colour.lower())
#     if individual_category != "NA":
#         filters.append(lambda point: point.payload.get("Individual_category", "").lower() == individual_category.lower())
#     if category != "NA":
#         filters.append(lambda point: point.payload.get("Category", "").lower() == category.lower())
#     if category_by_gender != "NA":
#         filters.append(lambda point: point.payload.get("category_by_Gender", "").lower() == category_by_gender.lower())

#     # Retrieve all points
#     all_points = []
#     next_page = None

#     while True:
#         response, next_page = client.scroll(
#             collection_name=COLLECTION_NAME,
#             limit=1000,
#             offset=next_page
#         )
#         all_points.extend(response)
#         if not next_page:
#             break

#     print(f"\n📦 Total Points Retrieved from Qdrant: {len(all_points)}")

#     # Show top 5 payloads for inspection
#     print("\n🔍 Sample Qdrant Payloads:")
#     for point in all_points[:5]:
#         print(point.payload)

#     # Filter and show why a point didn't match (debug only)
#     filtered_points = []
#     for point in all_points:
#         reasons = []
#         payload = point.payload

#         if colour != "NA" and payload.get("colour", "").lower() != colour.lower():
#             reasons.append(f"❌ colour mismatch: {payload.get('colour')} != {colour}")
#         if individual_category != "NA" and payload.get("Individual_category", "").lower() != individual_category.lower():
#             reasons.append(f"❌ individual_category mismatch: {payload.get('Individual_category')} != {individual_category}")
#         if category != "NA" and payload.get("Category", "").lower() != category.lower():
#             reasons.append(f"❌ category mismatch: {payload.get('Category')} != {category}")
#         if category_by_gender != "NA" and payload.get("category_by_Gender", "").lower() != category_by_gender.lower():
#             reasons.append(f"❌ gender mismatch: {payload.get('category_by_Gender')} != {category_by_gender}")

#         if not reasons:
#             filtered_points.append(point)
#         else:
#             # Uncomment to see why it failed
#             # print(f"\n🛑 Excluded: {payload['name']}\n" + "\n".join(reasons))
#             pass

#     # Fallback if no match
#     if not filtered_points:
#         print("\n⚠️ No exact matches found. Returning random 10 from all data.")
#         filtered_points = random.sample(all_points, min(10, len(all_points)))

#     results = [point.payload for point in filtered_points]
#     return results