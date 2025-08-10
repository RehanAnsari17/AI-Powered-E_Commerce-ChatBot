from qdrant_client import QdrantClient
from config import CLUSTER_URL, COLLECTION_NAME, QDRANT_API_KEY
from qdrant_client.models import Filter, FieldCondition, MatchValue, MinShould
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from typing import List, Optional, Dict, Any
import os
import requests
from qdrant_client.http import models
# Load environment variables
load_dotenv()

# Initialize Qdrant client
client = QdrantClient(
    url=CLUSTER_URL,
    api_key=QDRANT_API_KEY
)

# SentenceTransformer model (768-dim)
model = SentenceTransformer("all-MiniLM-L6-v2")

# ------------------- 🧠 CALL YOUR LLM -------------------

def call_llm_for_metadata(query_text):
    """
    Replace this function with your actual GROQ or custom LLM call
    that parses natural language into structured metadata.
    """
    print(f"🧠 Calling LLM to extract metadata from: {query_text}")

    try:
        # Example API call to a FastAPI or Flask backend that returns structured filters
        response = requests.post("http://localhost:8000/parse", json={"query": query_text})
        response.raise_for_status()
        parsed = response.json()

        return {
            "colour": parsed.get("colour", "NA"),
            "individual_category": parsed.get("individual_category", "NA"),
            "category": parsed.get("category", "NA"),
            "category_by_gender": parsed.get("category_by_gender", "NA")
        }

    except Exception as e:
        print("❌ LLM call failed:", str(e))
        return {
            "colour": "NA",
            "individual_category": "NA",
            "category": "NA",
            "category_by_gender": "NA"
        }

# ------------------- 🧠 GENERATE EMBEDDING -------------------

def generate_embedding(query_text):
    return model.encode(query_text).tolist()

# ------------------- 🔍 HYBRID SEARCH FUNCTION -------------------
def search_collection(query_text, colour, individual_category, category, category_by_gender, top_k=50):
    print(f"\n🔍 Incoming Filters - Colour: {colour}, Category: {category}, Individual: {individual_category}, Gender: {category_by_gender}")
    
    # Generate vector
    try:
        vector = model.encode(query_text).tolist()
        print(f"📡 SentenceTransformer embedding generated. Vector length: {len(vector)}")
    except Exception as e:
        print(f"❌ Error generating embedding: {e}")
        return []

    # Map article types to database values
    article_type_mapping = {
        "saree": ["Saree", "saree", "Sarees", "sarees", "Sari", "sari"],
        "kurtas": ["Kurtas", "kurtas", "Kurta", "kurta", "Kurta Sets", "kurta sets"],
        "kurtis": ["Kurtis", "kurtis", "Kurti", "kurti"],
        "jeans": ["Jeans", "jeans", "Jean", "jean"],
        "skirts": ["Skirts", "skirts", "Skirt", "skirt"],
        "tops": ["Tops", "tops", "Top", "top"],
        "shorts": ["Shorts", "shorts", "Short", "short"],
        "trousers": ["Trousers", "trousers", "Trouser", "trouser"],
        "jumpsuit": ["Jumpsuit", "jumpsuit", "Jumpsuits", "jumpsuits"],
        "ethnic-dresses": ["Dresses", "dresses", "Dress", "dress", "Ethnic Dresses", "ethnic dresses"],
        "traditional-wear": ["Traditional", "traditional", "Ethnic", "ethnic", "Indian Wear", "indian wear"]
    }

    must_filters = []
    should_filters = []
    
    # Add colour filter if specified
    if colour != "NA":
        must_filters.append(models.FieldCondition(
            key="baseColour",
            match=models.MatchValue(value=colour)
        ))
        print(f"🎨 Added colour filter: {colour}")

    # Add article type filter with mapping
    if individual_category != "NA":
        mapped_types = article_type_mapping.get(individual_category.lower(), [individual_category])
        if mapped_types:
            must_filters.append(models.FieldCondition(
                key="articleType",
                match=models.MatchAny(any=mapped_types)
            ))
            print(f"👕 Added article type filter: {mapped_types}")
        else:
            print(f"⚠️ No mapping found for article type: {individual_category}")

    # Add category filter as should (boosted but not required)
    if category != "NA":
        should_filters.append(models.FieldCondition(
            key="masterCategory",
            match=models.MatchValue(value=category)
        ))
        print(f"🏷️ Added category filter: {category}")
    
    # Add gender filter as should (boosted but not required)
    if category_by_gender != "NA":
        should_filters.append(models.FieldCondition(
            key="gender",
            match=models.MatchValue(value=category_by_gender)
        ))
        print(f"👤 Added gender filter: {category_by_gender}")

    combined_filter = models.Filter(
        must=must_filters,
        should=should_filters,
        must_not=[]
    )

    print(f"🔍 Total filters: {len(must_filters)} must, {len(should_filters)} should")
    print("📥 Performing hybrid search with filters...")

    try:
        search_result = client.search(
            collection_name="my_collection",
            query_vector=vector,
            limit=top_k,
            with_payload=True,
            score_threshold=None,
            query_filter=combined_filter
        )
    except Exception as e:
        print(f"❌ Qdrant hybrid search failed: {e}")
        search_result = []

    results = []
    seen_ids = set()

    for item in search_result:
        if item.payload is not None:
            product_id = item.payload.get("id")
            if product_id not in seen_ids:
                result = item.payload
                result["score"] = item.score
                results.append(result)
                seen_ids.add(product_id)

    if results:
        print(f"✅ Found {len(results)} products with hybrid search.")
        # Sort by relevance score and return top results
        results.sort(key=lambda x: x.get("score", 0), reverse=True)
        return results[:top_k]

    # 🔁 Fallback: Try with only essential filters (colour + article type)
    print("⚠️ No matching products found with all filters. Trying with essential filters...")
    essential_filters = []
    
    if colour != "NA":
        essential_filters.append(models.FieldCondition(
            key="baseColour",
            match=models.MatchValue(value=colour)
        ))
    
    if individual_category != "NA":
        mapped_types = article_type_mapping.get(individual_category.lower(), [individual_category])
        if mapped_types:
            essential_filters.append(models.FieldCondition(
                key="articleType",
                match=models.MatchAny(any=mapped_types)
            ))
    
    if essential_filters:
        try:
            fallback_result = client.search(
                collection_name="my_collection",
                query_vector=vector,
                limit=top_k,
                with_payload=True,
                score_threshold=None,
                query_filter=models.Filter(must=essential_filters)
            )
            
            for item in fallback_result:
                if item.payload is not None:
                    product_id = item.payload.get("id")
                    if product_id not in seen_ids:
                        result = item.payload
                        result["score"] = item.score
                        results.append(result)
                        seen_ids.add(product_id)
            
            if results:
                print(f"🔁 Essential filters found {len(results)} products.")
                results.sort(key=lambda x: x.get("score", 0), reverse=True)
                return results[:top_k]
        except Exception as e:
            print(f"❌ Essential filters search failed: {e}")

    # 🔄 Final fallback: vector-only search with relevance scoring
    print("🔄 No products found with filters. Using vector-only search...")
    try:
        final_fallback = client.search(
            collection_name="my_collection",
            query_vector=vector,
            limit=top_k * 2,  # Get more results for better selection
            with_payload=True,
            score_threshold=None
        )
        
        # Filter results to prioritize products that might be related
        for item in final_fallback:
            if item.payload is not None:
                product_id = item.payload.get("id")
                if product_id not in seen_ids:
                    result = item.payload
                    result["score"] = item.score
                    
                    # Boost score for products that might be related
                    article_type = result.get("articleType", "").lower()
                    if any(keyword in query_text.lower() for keyword in ["saree", "kurta", "kurti", "dress", "ethnic"]):
                        if any(keyword in article_type for keyword in ["saree", "kurta", "kurti", "dress", "ethnic", "traditional"]):
                            result["score"] *= 1.5  # Boost relevant products
                    
                    results.append(result)
                    seen_ids.add(product_id)
        
        if results:
            print(f"🔄 Vector-only search found {len(results)} products.")
            # Sort by boosted score and return top results
            results.sort(key=lambda x: x.get("score", 0), reverse=True)
            return results[:top_k]
            
    except Exception as e:
        print(f"❌ Final fallback search failed: {e}")
        return []

    return []


# ------------------- 📜 FILTER-ONLY (SCROLL) FETCH -------------------
def fetch_by_filters(
    *,
    article_types: Optional[List[str]] = None,
    base_colour: Optional[str] = None,
    gender: Optional[str] = None,
    limit: int = 200,
) -> List[Dict[str, Any]]:
    """
    Fetch products from Qdrant using ONLY metadata filters (no vector search),
    returning up to `limit` payloads. Uses scroll under the hood and supports
    large result sets (1k+).

    - article_types: list of acceptable values for `articleType` (e.g., ["Kurtis", "Kurtas"]).
    - base_colour: single colour value (case-sensitive in Qdrant, so pass Title case like "Blue").
    - gender: "Women" | "Men" (Title case recommended to match dataset).
    - limit: max number of items to return.
    """

    must_filters: List[models.FieldCondition] = []

    if article_types:
        # Match any of multiple article types (e.g., Kurtis/Kurtas/Kurta Sets)
        must_filters.append(
            models.FieldCondition(
                key="articleType",
                match=models.MatchAny(any=article_types),
            )
        )

    if base_colour:
        must_filters.append(
            models.FieldCondition(
                key="baseColour",
                match=models.MatchValue(value=base_colour),
            )
        )

    if gender:
        must_filters.append(
            models.FieldCondition(
                key="gender",
                match=models.MatchValue(value=gender),
            )
        )

    metadata_filter = models.Filter(must=must_filters, should=[], must_not=[])

    collected: list[dict] = []
    next_offset = None

    # Scroll in chunks to gather large result sets
    while len(collected) < limit:
        page_limit = min(256, limit - len(collected))
        points, next_offset = client.scroll(
            collection_name="my_collection",
            scroll_filter=metadata_filter,
            with_payload=True,
            with_vectors=False,
            limit=page_limit,
            offset=next_offset,
        )

        if not points:
            break

        for p in points:
            if p.payload:
                collected.append(p.payload)
                if len(collected) >= limit:
                    break

        if not next_offset:
            break

    return collected


def fetch_by_filters_page(
    *,
    article_types: Optional[List[str]] = None,
    base_colour: Optional[str] = None,
    gender: Optional[str] = None,
    limit: int = 48,
    offset: Optional[Any] = None,
) -> Dict[str, Any]:
    """
    Scroll a single page using Qdrant filter-only query.
    Returns dict with keys: { 'items': List[payload], 'next_offset': token or None }
    Pass the returned next_offset back to continue scrolling.
    """
    must_filters: List[models.FieldCondition] = []

    if article_types:
        must_filters.append(
            models.FieldCondition(
                key="articleType",
                match=models.MatchAny(any=article_types),
            )
        )

    if base_colour:
        must_filters.append(
            models.FieldCondition(
                key="baseColour",
                match=models.MatchValue(value=base_colour),
            )
        )

    if gender:
        must_filters.append(
            models.FieldCondition(
                key="gender",
                match=models.MatchValue(value=gender),
            )
        )

    metadata_filter = models.Filter(must=must_filters, should=[], must_not=[])

    points, next_offset = client.scroll(
        collection_name="my_collection",
        scroll_filter=metadata_filter,
        with_payload=True,
        with_vectors=False,
        limit=limit,
        offset=offset,
    )

    items: List[Dict[str, Any]] = []
    for p in points:
        if p.payload:
            items.append(p.payload)

    return {"items": items, "next_offset": next_offset}

















# from qdrant_client import QdrantClient
# from config import CLUSTER_URL, COLLECTION_NAME, QDRANT_API_KEY
# from qdrant_client.models import Filter, FieldCondition, MatchValue ,MinShould
# from dotenv import load_dotenv
# from sentence_transformers import SentenceTransformer
# import os

# # Load environment variables
# load_dotenv()

# # Initialize Qdrant client
# client = QdrantClient(
#     url=CLUSTER_URL,
#     api_key=QDRANT_API_KEY
# )

# # Initialize SentenceTransformer model (384-dim)
# model = SentenceTransformer("all-MiniLM-L6-v2")

# def generate_embedding(query_text):
#     return model.encode(query_text).tolist()  # Ensure it's a plain list




# def search_collection(query_text="", colour="NA", individual_category="NA", category="NA", category_by_gender="NA"):
#     print(f"\n📥 Incoming Filters - Colour: {colour}, Category: {category}, Individual: {individual_category}, Gender: {category_by_gender}")
    
#     try:
#         query_vector = generate_embedding(query_text)
#         print("📡 SentenceTransformer embedding generated.")
#     except Exception as e:
#         print("❌ Error generating embedding:", str(e))
#         return []

#     # -------- Separate must and should filters --------
#     must_conditions = []
#     should_conditions = []

#     if category_by_gender != "NA":
#         must_conditions.append(FieldCondition(key="gender", match=MatchValue(value=category_by_gender)))
#     if category != "NA":
#         must_conditions.append(FieldCondition(key="masterCategory", match=MatchValue(value=category)))

#     if colour != "NA":
#         should_conditions.append(FieldCondition(key="baseColour", match=MatchValue(value=colour)))
#     if individual_category != "NA":
#         should_conditions.append(FieldCondition(key="articleType", match=MatchValue(value=individual_category)))

#     metadata_filter = None
#     if must_conditions or should_conditions:
#         if should_conditions:
#             metadata_filter = Filter(
#                 must=must_conditions if must_conditions else None,
#                 must_not=None,
#                 min_should=MinShould(conditions=should_conditions, min_count=1)
#             )
#         else:
#             metadata_filter = Filter(
#                 must=must_conditions if must_conditions else None,
#                 must_not=None
#             )    

#     try:
#         search_result = client.search(
#             collection_name=COLLECTION_NAME,
#             query_vector=query_vector,
#             limit=10,
#             query_filter=metadata_filter
#         )

#         if search_result:
#             print(f"🛍️ Products Found: {len(search_result)}")
#             payloads = [point.payload for point in search_result]
#         else:
#             print("⚠️ No matching products found with filters. Trying fallback (vector-only)...")
#             fallback_result = client.search(
#                 collection_name=COLLECTION_NAME,
#                 query_vector=query_vector,
#                 limit=10
#             )
#             print(f"🔁 Fallback results: {len(fallback_result)}")
#             payloads = [point.payload for point in fallback_result]

#         # ✅ Remove duplicates by ID
#         seen_ids = set()
#         unique_results = []
#         for item in payloads:
#             if item is not None and 'id' in item and item['id'] not in seen_ids:
#                 unique_results.append(item)
#                 seen_ids.add(item['id'])

#         return unique_results

#     except Exception as e:
#         print("❌ Qdrant search failed:", str(e))
#         return []


