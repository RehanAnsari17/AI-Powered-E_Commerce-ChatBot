import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Step 1: Load environment variables from .env
load_dotenv()

# Step 2: Fetch the API key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("❌ GROQ_API_KEY not found in environment. Check your .env file.")
    exit(1)

print("✅ GROQ_API_KEY loaded successfully.")

# Step 3: Try initializing the Groq LLM
try:
    llm = ChatGroq(
        api_key=api_key,
        model_name="llama3-8b-8192"  # or "llama3-70b-8192" if that's what you're using
    )

    # Step 4: Send a test prompt
    response = llm.invoke("Hello, what is the capital of France?")
    print("✅ API call successful. Response:")
    print(response.content)

except Exception as e:
    print("❌ Error connecting to Groq API:")
    print(e)
