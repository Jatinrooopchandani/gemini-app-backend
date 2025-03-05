from flask import Flask, jsonify, request
from google import genai
import urllib.parse
from dotenv import load_dotenv
import os
from supabase import create_client, Client
import jwt
load_dotenv()
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_ANON_KEY")
supabase: Client = create_client(url, key)
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")

app = Flask(__name__)
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("Missing API Key")
client = genai.Client(api_key=API_KEY)

@app.route('/data', methods=['GET'])
def data():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Unauthorized: Missing token"}), 401
    token = auth_header.split("Bearer ")[1]
    user_response = supabase.auth.get_user(token)
    
    user_data = user_response.user
    print("✅ Authenticated User:", user_data)
    print(user_data)
    encoded_prompt = request.args.get("prompt")
    if not encoded_prompt:
            return jsonify({"error": "Missing prompt"}), 400
    prompt = urllib.parse.unquote(encoded_prompt)
    response = client.models.generate_content(
        model = "gemini-2.0-flash",
        contents = prompt
    )
    return jsonify({"response": response.text})