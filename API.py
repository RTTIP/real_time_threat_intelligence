from flask import Flask, jsonify, request
from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import requests
import json

app = Flask(__name__)

# PostgreSQL Database setup
DATABASE_URL = 'postgresql://myuser:mypassword@localhost/mydatabase'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Define model for storing API data
class APIData(Base):
    __tablename__ = 'api_data'
    id = Column(Integer, primary_key=True)
    source = Column(String, nullable=False)
    data = Column(JSON, nullable=False)

# Create tables
Base.metadata.create_all(engine)

# Helper function to fetch data from APIs
def fetch_api_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None

# Endpoint to trigger data fetching and storing
@app.route('/fetch_and_store', methods=['POST'])
def fetch_and_store():
    api_url_1 = 'https://api1.example.com/data'
    api_url_2 = 'https://api2.example.com/data'
    
    data_1 = fetch_api_data(api_url_1)
    data_2 = fetch_api_data(api_url_2)
    
    if data_1 and data_2:
        with Session() as session:
            session.add_all([
                APIData(source='API 1', data=data_1),
                APIData(source='API 2', data=data_2)
            ])
            session.commit()
        return jsonify({"message": "Data stored successfully"}), 200
    else:
        return jsonify({"message": "Failed to fetch data from one or both APIs"}), 500

# Endpoint to retrieve stored data
@app.route('/get_stored_data', methods=['GET'])
def get_stored_data():
    with Session() as session:
        data = session.query(APIData).all()
        return jsonify([
            {"source": item.source, "data": item.data}
            for item in data
        ]), 200

if __name__ == '__main__':
    app.run(debug=True)
