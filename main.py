from flask import Flask
from flask_pymongo import PyMongo
from routes.routes import register_routes

app = Flask(__name__)

# MongoDB connection details
app.config["MONGO_URI"] = "mongodb+srv://bka2bg:QcqSyZpNSyiH52cU@crisismanagement.vypxy.mongodb.net/Crisis_Management"
mongo = PyMongo(app)

register_routes(app, mongo)

if __name__ == "__main__":
    app.run(debug=True)
