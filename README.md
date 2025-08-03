E_Commerce-ChatBot 🤖

Introduction:-

Welcome to the RehanAnsari17/AI-Powered-E_Commerce-ChatBot repository. This project demonstrates an AI-powered chatbot designed to enhance e-commerce experiences by providing personalized fashion recommendations. The chatbot leverages state-of-the-art natural language processing and semantic vector search to help users discover the perfect outfits based on their conversational queries. The project utilizes the Flask web framework, integrates with Qdrant for efficient vector storage and retrieval, and uses the Sentence Transformers model for embeddings generation. Additionally, the chatbot uses Langchain for prompt orchestration with ChatGroq to facilitate engaging conversations with users.

Features

Conversational Recommendations: Chat with the bot to receive tailored fashion product recommendations.
Hybrid Search: Combines metadata filtering with a hybrid vector search over product descriptions and images, ensuring high-quality matching results.
Qdrant Integration: Uses Qdrant as the vector database to store and query high-dimensional embeddings for product data.
Image and Metadata Upload: Includes scripts to upload images with embedded metadata to Cloudinary, while mapping these URLs to the Qdrant collection.
Kaggle Dataset Usage: Utilizes the Kaggle Myntra dataset for chatbot recommendation generation. You can find the dataset at https://www.kaggle.com/datasets/hiteshsuthar101/myntra-fashion-product-dataset/data fileciteturn0file1.
Intuitive Front-End: Contains user-friendly HTML templates and JavaScript functionality to offer an engaging and interactive experience.
Easy Deployment: Built with Flask for seamless deployment on any server supporting Python web applications.
Installation

Clone the Repository: Clone the repository using Git: code git clone https://github.com/RehanAnsari17/AI-Powered-E_Commerce-ChatBot.git code end

Create a Virtual Environment: It is recommended to use a virtual environment to manage dependencies. code python -m venv venv source venv/bin/activate # On Windows: venv\Scripts\activate code end

Install Dependencies: Install all required dependencies using pip: code pip install -r requirements.txt code end

Environment Configuration: Create a .env file in the root directory and set the following environment variables:

CLUSTER_URL: URL for the Qdrant cluster.
QDRANT_API_KEY: Your Qdrant API key.
COLLECTION_NAME: Collection name for the products.
CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, and CLOUDINARY_API_SECRET if you are uploading images.
GROQ_API_KEY: API key for ChatGroq (if applicable).
Configure Dataset: The project uses the Kaggle Myntra dataset for recommendation generation. Download the dataset from the provided URL https://www.kaggle.com/datasets/hiteshsuthar101/myntra-fashion-product-dataset/data, and place the dataset files in the appropriate folder as referenced in the code.

Initialize Qdrant Collection: Run the script to create or reset the Qdrant collection: code python init_collection.py code end

Usage

Run the Application: Start the Flask server by running the main application: code python app.py code end The application will be accessible at http://127.0.0.1:5000, where you can interact with the chatbot.

Chatbot Interaction: Navigate to /chatbot for the chatbot interface. Enter your query related to fashion products, such as types of dresses, sarees, or accessories. The application will parse your conversation, extract relevant metadata, perform a hybrid search, and return a list of recommended products based on the products dataset.

Product Recommendations: The backend uses a combination of hybrid vector search and metadata filtering to present recommendations in a visually appealing layout (HTML/CSS). The recommendations are based on user queries and include details like product images, names, and prices.

Cloudinary and Qdrant Integration:

Use the update_cloud.py script to upload product images with metadata to Cloudinary.
Use the update_qdrant_urls.py script to update Qdrant with new Cloudinary URLs for the corresponding product images.
Troubleshooting and Logs: Monitor the terminal outputs and logs for detailed information on data uploads, embedding generation, and API interactions. Debug messages help identify steps that have successfully run (e.g., successful batch uploads reported from Qdrant and Cloudinary) as seen in the source code (fileciteturn0file2, fileciteturn0file4).
