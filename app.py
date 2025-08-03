from src.searcher import search_collection
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
# print("Api_Key:", api_key)
# Initialize LLM
llm = ChatGroq(
    temperature = TEMPERATURE,
    groq_api_key = api_key,
    model_name = "llama3-8b-8192"
)

# ---------- ROUTES ----------

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/chatbot')
def chatbot():
    return render_template('index.html')

@app.route('/wishlist')
def wishlist():
    return render_template('wishlist.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/skirts')
def skirts():
    return render_template('skirts.html')

@app.route('/jeans')
def jeans():
    return render_template('jeans.html')

@app.route('/jumpsuits')
def jumpsuits():
    return render_template('jumpsuits.html')

@app.route('/kurtis')
def kurtis():
    return render_template('kurtis.html')

@app.route('/store')
def store():
    return render_template('store.html')

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/product')
def product():
    return render_template('product.html')

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
