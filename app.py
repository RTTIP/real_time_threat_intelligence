from flask import Flask
from config.db import initialize_db
from routes.threat_analysis_controller import analysis_bp
import os

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("mongodb://localhost:27017/ThreatIntelligenceDB")

# Initialize database and register routes
initialize_db(app)
app.register_blueprint(analysis_bp, url_prefix="/api/v1/threats")

if __name__ == "__main__":
    app.run(debug=True)

