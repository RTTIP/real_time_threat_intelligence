from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)

# MongoDB connection details
app.config["MONGO_URI"] = "mongodb+srv://bka2bg:QcqSyZpNSyiH52cU@crisismanagement.vypxy.mongodb.net/Crisis_Management"
mongo = PyMongo(app)

@app.route("/api/documents", methods=["GET"])
def get_documents():
    documents = list(mongo.db.crisismanagement.find())
    for doc in documents:
        doc['_id'] = str(doc['_id'])
    return jsonify(documents)

@app.route("/api/documents", methods=["POST"])
def create_document():
    data = request.get_json()
    result = mongo.db.crisismanagement.insert_one(data)
    return jsonify({"id": str(result.inserted_id)}), 201
