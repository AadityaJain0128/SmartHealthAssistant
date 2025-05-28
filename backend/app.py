from flask import Flask, jsonify, request
from dotenv import load_dotenv
from os import environ
import requests
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta, datetime
from flask_cors import CORS


load_dotenv()
API_KEY = environ.get("API_KEY")
API_URL = environ.get("API_URL")
SYSTEM_PROMPT = environ.get("SYSTEM_PROMPT")
JWT_SECRET_KEY = environ.get("JWT_SECRET_KEY")
MONGO_URI = environ.get("MONGO_URI")

app = Flask(__name__)
app.config["MONGO_URI"] = MONGO_URI
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
mongo = PyMongo(app)
jwt = JWTManager(app)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)


@app.route("/")
def home():
    return "Hello"


@app.post("/signup")
def signup():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    
    existing_user = mongo.db.users.find_one({"username": username})
    if existing_user:
        return jsonify({"error": "Username already exists"}), 400
    
    hashed_password = generate_password_hash(password)
    mongo.db.users.insert_one({"username": username, "password": hashed_password})
    return jsonify({"message": "User registered successfully"}), 201

@app.post("/login")
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    
    user = mongo.db.users.find_one({"username": username})
    if not user or not check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid credentials"}), 401
    
    access_token = create_access_token(identity=username, expires_delta=timedelta(days=5))
    return jsonify({"access_token": access_token}), 200


@app.post("/chat")
@jwt_required()
def chat():
    data = request.json
    user_message = data.get("message")
    username = get_jwt_identity()
    
    if not user_message:
        return jsonify({"error": "Message is required"}), 400
    
    response = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        json={
            "model": "llama3-70b-8192",
            "messages": [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        }
    )
    
    if response.status_code == 200:
        bot_reply = response.json().get("choices", [{}])[0].get("message", {}).get("content", "No response")
        
        # Store chat in MongoDB
        chat_entry = {
            "username": username,
            "message": user_message,
            "response": bot_reply,
            "timestamp": datetime.now()
        }
        mongo.db.chats.insert_one(chat_entry)
        
        return jsonify({"response": bot_reply})
    else:
        return jsonify({"error": "Failed to fetch response from Groq API"}), response.status_code


@app.get("/chats")
@jwt_required()
def get_chats():
    username = get_jwt_identity()
    chats = list(mongo.db.chats.find({"username": username}, {"_id": 0}))
    return jsonify({"chats": chats})

if __name__ == '__main__':
    app.run(debug=True)
