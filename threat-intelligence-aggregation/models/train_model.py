import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.preprocessing import LabelEncoder
import numpy as np
import joblib

# Load preprocessed threat data
data = pd.read_csv('virustotal.csv')

# 1. Process 'description' text data with TF-IDF
vectorizer = TfidfVectorizer(max_features=500)
description_vectors = vectorizer.fit_transform(data['description']).toarray()

# 2. Process 'severity' as a numerical feature
severity = data['severity'].values

# 3. Process 'indicators' to count the number of indicators
num_indicators = data['indicators'].apply(lambda x: len(x.split(',')) if pd.notnull(x) else 0).values

# Encode 'type' as the target label for classification
label_encoder = LabelEncoder()
category = label_encoder.fit_transform(data['type'])  # Category labels for classification

# Combine features into a single array
X = np.concatenate([description_vectors, severity.reshape(-1, 1), num_indicators.reshape(-1, 1)], axis=1)

# Split data for both models
X_train, X_test, y_train_category, y_test_category = train_test_split(X, category, test_size=0.2, random_state=42)
_, _, y_train_risk, y_test_risk = train_test_split(X, severity, test_size=0.2, random_state=42)  # Use severity as risk score

# Initialize and train the classification model
category_model = RandomForestClassifier(n_estimators=100, random_state=42)
category_model.fit(X_train, y_train_category)

# Initialize and train the regression model for risk score
risk_model = RandomForestRegressor(n_estimators=100, random_state=42)
risk_model.fit(X_train, y_train_risk)

# Evaluate the models
category_pred = category_model.predict(X_test)
risk_pred = risk_model.predict(X_test)
category_accuracy = accuracy_score(y_test_category, category_pred)
risk_mse = mean_squared_error(y_test_risk, risk_pred)
print(f"Category Model Accuracy: {category_accuracy * 100:.2f}%")
print(f"Risk Model Mean Squared Error: {risk_mse:.2f}")

# Save both models and vectorizer
joblib.dump(category_model, 'category_model.pkl')
joblib.dump(risk_model, 'risk_model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')
joblib.dump(label_encoder, 'label_encoder.pkl')  # Save the label encoder for decoding category predictions
