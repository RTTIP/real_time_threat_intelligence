from flask import jsonify, render_template, request
import requests

def register_routes(app, mongo):
    @app.route("/", methods=["GET", "POST"])
    def home():
        if request.method == "POST":
            # Get form data
            new_document = {
                "title": request.form.get("title"),
                "severity": request.form.get("severity"),
                "status": request.form.get("status"),
                "description": request.form.get("description"),
                "type": request.form.get("type"),
                "location": request.form.get("location"),
                "affected_assets": request.form.getlist("affected_assets"),
                "resolution_time": request.form.get("resolution_time")
            }
            # Send POST request to FastAPI
            response = requests.post("http://127.0.0.1:8000/api/documents", json=new_document)
            if response.status_code == 200:
                return redirect(url_for('home'))
        
        # Fetch all documents from the collection
        documents = list(mongo.db.crisismanagement.find())
        
        # Convert ObjectId to string for JSON serialization
        for doc in documents:
            doc['_id'] = str(doc['_id'])
        
        return render_template('index.html', documents=documents)
