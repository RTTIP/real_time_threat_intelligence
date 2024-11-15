from flask import Flask, jsonify
from config.db import mongo, initialize_db
from routes.threat_routes import threat_bp
from flask_cors import CORS
from routes.llm_summary_routes import summary_bp


app = Flask(__name__)

CORS(app)

app.config["MONGO_URI"] = "mongodb://localhost:27017/ThreatIntelligenceDB"

try:
    initialize_db(app)
except Exception as e:
    print(f"Error initializing database: {e}")
    # Handle logging or graceful shutdown as needed

# Register the blueprint for threat routes
app.register_blueprint(threat_bp, url_prefix='/api/v1/threats')
app.register_blueprint(summary_bp, url_prefix='/api/v1/llm')


# Test route for MongoDB integration
@app.route('/test_db')
def test_db():
    try:
        # Attempt to find one document in the 'threats' collection
        test_document = mongo.db.threats.find_one()
        if test_document:
            return jsonify({"message": "MongoDB connected successfully!", "sample_document": test_document}), 200
        else:
            return jsonify({"message": "MongoDB connected, but no data found in 'threats' collection."}), 200
    except Exception as e:
        return jsonify({"error": f"Error connecting to MongoDB: {str(e)}"}), 500
    
@app.route('/')
def home():
    return "Welcome to the Threat Intelligence Aggregator API"

if __name__ == "__main__":
    app.run(debug=True)
