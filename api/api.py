from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from bson import ObjectId
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# MongoDB connection details
client = MongoClient("mongodb+srv://bka2bg:QcqSyZpNSyiH52cU@crisismanagement.vypxy.mongodb.net/Crisis_Management")
db = client["Crisis_Management"]
collection = db["crisismanagement"]

# Define Pydantic model for the document
class CrisisDocument(BaseModel):
    title: str
    severity: str
    status: str
    description: str
    type: str
    location: Optional[str] = None
    affected_assets: List[str] = []
    resolution_time: Optional[int] = None

@app.get("/api/documents")
def get_documents():
    documents = list(collection.find())
    for doc in documents:
        doc['_id'] = str(doc['_id'])
    return JSONResponse(content=documents)

@app.post("/api/documents")
def create_document(document: CrisisDocument):
    result = collection.insert_one(document.dict())
    return JSONResponse(content={"id": str(result.inserted_id)})
