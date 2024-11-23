from flask import Flask
from config.db import mongo, initialize_db
from routes.threat_routes import threat_bp
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

app.config["MONGO_URI"] = "mongodb+srv://threatintelligenceaggregation:module2@threat-intelligence-agg.vapqz.mongodb.net/ThreatIntelligenceDB?retryWrites=true&w=majority&appName=threat-intelligence-aggregation-cluster"

initialize_db(app)

app.register_blueprint(threat_bp, url_prefix='/api/v1/threats')

if __name__ == "__main__":
    app.run(debug=True)
