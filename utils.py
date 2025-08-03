from openai import OpenAI
import os

openai_api_key = os.getenv("OPENAI_API_KEY")  # set this in your .env
client = OpenAI(api_key=openai_api_key)

def get_embedding(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding