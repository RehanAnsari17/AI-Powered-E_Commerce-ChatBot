from src.searcher import search_collection
from src.searcher import fetch_by_filters, fetch_by_filters_page
from src.extractor import extractor
from src.parser import parser
from config import TEMPERATURE, MODEL_NAME  # GROQ_API_KEY removed here
from flask import Flask, request, jsonify, render_template
from langchain_groq import ChatGroq
import json
import random
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='templates')
api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    temperature = TEMPERATURE,
    groq_api_key = api_key,
    model_name = "llama3-8b-8192"
)

# ---------- ROUTES ----------

@app.route('/')
def home():
    return render_template('home_immersive.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot_3d.html')

@app.route('/wishlist')
def wishlist():
    return render_template('wishlist_3d.html')

@app.route('/cart')
def cart():
    return render_template('cart_3d.html')

@app.route('/skirts')
def skirts():
    return render_template('skirts_3d.html')

@app.route('/jeans')
def jeans():
    return render_template('jeans_3d.html')

@app.route('/jumpsuits')
def jumpsuits():
    return render_template('jumpsuits_3d.html')

@app.route("/kurtis")
def kurtis():
    return render_template("kurtis_3d.html")


@app.route("/api/kurtis", methods=["GET"])
def api_kurtis():
    # Query params: colour, gender, limit, page_offset
    colour = request.args.get("colour") or None
    gender = request.args.get("gender") or None
    limit = request.args.get("limit", default=1000, type=int)
    page_limit = request.args.get("page_limit", default=48, type=int)
    page_offset = request.args.get("page_offset")
    article_type = request.args.get("article_type") or None

    # Accept common variations as kurtis
    kurtis_like = [
        "Kurtis",
        "Kurtas",
        "Kurta Sets",
        "kurti",
        "kurtis",
        "kurtas",
        "kurta",
    ]

    if page_offset == "None":
        page_offset = None

    page = fetch_by_filters_page(
        article_types=[article_type] if article_type else kurtis_like,
        base_colour=colour,
        gender=gender,
        limit=page_limit,
        offset=page_offset,
    )

    # Normalize minimal fields for frontend expectation
    normalized = []
    for it in page["items"]:
        normalized.append({
            "id": it.get("id") or it.get("product_id") or it.get("name"),
            "image_url": it.get("image_url"),
            "gender": it.get("gender"),
            "masterCategory": it.get("masterCategory") or it.get("Category"),
            "subCategory": it.get("subCategory"),
            "articleType": it.get("articleType") or it.get("Individual_category"),
            "baseColour": it.get("baseColour") or it.get("colour"),
            "productDisplayName": it.get("productDisplayName") or it.get("name"),
        })

    return jsonify({"results": normalized, "next_offset": page.get("next_offset")})


@app.route("/api/skirts", methods=["GET"])
def api_skirts():
    colour = request.args.get("colour") or None
    gender = request.args.get("gender") or None
    page_limit = request.args.get("page_limit", default=48, type=int)
    page_offset = request.args.get("page_offset")
    article_type = request.args.get("article_type") or None
    if page_offset == "None":
        page_offset = None

    items_like = ["Skirts", "skirt", "skirts", "Mini Skirt", "Midi Skirt", "Maxi Skirt"]
    page = fetch_by_filters_page(
        article_types=[article_type] if article_type else items_like,
        base_colour=colour,
        gender=gender,
        limit=page_limit,
        offset=page_offset,
    )

    normalized = []
    for it in page["items"]:
        normalized.append({
            "id": it.get("id") or it.get("product_id") or it.get("name"),
            "image_url": it.get("image_url"),
            "gender": it.get("gender"),
            "masterCategory": it.get("masterCategory") or it.get("Category"),
            "subCategory": it.get("subCategory"),
            "articleType": it.get("articleType") or it.get("Individual_category"),
            "baseColour": it.get("baseColour") or it.get("colour"),
            "productDisplayName": it.get("productDisplayName") or it.get("name"),
        })

    return jsonify({"results": normalized, "next_offset": page.get("next_offset")})


@app.route("/api/jeans", methods=["GET"])
def api_jeans():
    colour = request.args.get("colour") or None
    gender = request.args.get("gender") or None
    page_limit = request.args.get("page_limit", default=48, type=int)
    page_offset = request.args.get("page_offset")
    article_type = request.args.get("article_type") or None
    if page_offset == "None":
        page_offset = None

    items_like = ["Jeans", "jeans", "Skinny Jeans", "Straight Jeans", "Bootcut Jeans", "Wide Leg Jeans"]
    page = fetch_by_filters_page(
        article_types=[article_type] if article_type else items_like,
        base_colour=colour,
        gender=gender,
        limit=page_limit,
        offset=page_offset,
    )

    normalized = []
    for it in page["items"]:
        normalized.append({
            "id": it.get("id") or it.get("product_id") or it.get("name"),
            "image_url": it.get("image_url"),
            "gender": it.get("gender"),
            "masterCategory": it.get("masterCategory") or it.get("Category"),
            "subCategory": it.get("subCategory"),
            "articleType": it.get("articleType") or it.get("Individual_category"),
            "baseColour": it.get("baseColour") or it.get("colour"),
            "productDisplayName": it.get("productDisplayName") or it.get("name"),
        })

    return jsonify({"results": normalized, "next_offset": page.get("next_offset")})


@app.route("/api/jumpsuits", methods=["GET"])
def api_jumpsuits():
    colour = request.args.get("colour") or None
    gender = request.args.get("gender") or None
    page_limit = request.args.get("page_limit", default=48, type=int)
    page_offset = request.args.get("page_offset")
    article_type = request.args.get("article_type") or None
    if page_offset == "None":
        page_offset = None

    items_like = ["Jumpsuit", "Jumpsuits", "jumpsuit", "jumpsuits"]
    page = fetch_by_filters_page(
        article_types=[article_type] if article_type else items_like,
        base_colour=colour,
        gender=gender,
        limit=page_limit,
        offset=page_offset,
    )

    normalized = []
    for it in page["items"]:
        normalized.append({
            "id": it.get("id") or it.get("product_id") or it.get("name"),
            "image_url": it.get("image_url"),
            "gender": it.get("gender"),
            "masterCategory": it.get("masterCategory") or it.get("Category"),
            "subCategory": it.get("subCategory"),
            "articleType": it.get("articleType") or it.get("Individual_category"),
            "baseColour": it.get("baseColour") or it.get("colour"),
            "productDisplayName": it.get("productDisplayName") or it.get("name"),
        })

    return jsonify({"results": normalized, "next_offset": page.get("next_offset")})

@app.route('/store')
def store():
    return render_template('store_3d.html')

@app.route('/checkout')
def checkout():
    return render_template('checkout_3d.html')

@app.route('/product')
def product():
    return render_template('product.html')

@app.route('/order-confirmation')
def order_confirmation():
    return render_template('order_confirmation.html')

# ---------- SEARCH API ----------

@app.route('/search', methods=['POST'])
def search():
    try:
        data = request.json
        query = data.get('query', '')

        if not query.strip():
            return jsonify({"results": [], "message": "Please provide a query."}), 400

        # Step 1: Extract + Parse query
        extracted_response = extractor(llm, query)
        print("\n🔍 Raw LLM Response:\n", extracted_response)

        parsed_data = parser(extracted_response)
        print("\n✅ Parsed Data:", parsed_data)

        if parsed_data.get("MOVE_ON"):
            # Step 2: Hybrid vector + metadata search
            results = search_collection(
                query_text=query,
                colour=parsed_data.get("colour", "NA"),
                individual_category=parsed_data.get("Individual_category", "NA"),
                category=parsed_data.get("Category", "NA"),
                category_by_gender=parsed_data.get("category_by_Gender", "NA")
            )

            return jsonify({
                "results": results,
                "message": "Here are some recommended products based on your query."
            })

        else:
            return jsonify({
                "results": [],
                "message": parsed_data.get("FOLLOW_UP_MESSAGE", "Please provide more product details.")
            })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            "results": [],
            "error": f"Internal Server Error: {str(e)}"
        }), 500

# ---------- RUN ----------

if __name__ == '__main__':
    app.run(debug=True)
