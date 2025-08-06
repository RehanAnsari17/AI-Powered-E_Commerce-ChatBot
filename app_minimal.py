from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import random
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# ---------- ROUTES ----------

@app.route('/')
def home():
    return render_template('home_new.html')

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

# ---------- SEARCH API (Simplified) ----------

@app.route('/search', methods=['POST'])
def search():
    try:
        data = request.json
        query = data.get('query', '')

        if not query.strip():
            return jsonify({"results": [], "message": "Please provide a query."}), 400

        # Simplified mock response for now
        mock_results = [
            {
                "id": 1,
                "name": "Sample Product",
                "price": "$29.99",
                "image_url": "/static/images_previous/products/sample.jpg",
                "description": "This is a sample product for demonstration"
            }
        ]

        return jsonify({
            "results": mock_results,
            "message": f"Showing mock results for '{query}'. Full AI search functionality requires additional dependencies."
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
    app.run(debug=True, host='0.0.0.0', port=5000)
