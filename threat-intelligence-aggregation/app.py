from flask import Flask
from config.db import mongo, initialize_db
from routes.threat_routes import threat_bp
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

app.config["MONGO_URI"] = "mongodb://localhost:27017/ThreatIntelligenceDB"

try:
    initialize_db(app)
except Exception as e:
    print(f"Error initializing database: {e}")
    # Handle logging or graceful shutdown as needed


app.register_blueprint(threat_bp, url_prefix='/api/v1/threats')

if __name__ == "__main__":
    app.run(debug=True)
