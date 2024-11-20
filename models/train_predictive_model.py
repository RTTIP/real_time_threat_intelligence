import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score 
import joblib

# Load historical threat data
try:
    data = pd.read_csv("models/historical_threat_data.csv")  # Ensure this path is correct
    print("Dataset loaded successfully!")
except FileNotFoundError:
    print("Error: The file 'historical_threat_data.csv' was not found. Please ensure the file exists.")
    exit()

# Feature Engineering
# Assuming 'indicators' is a string column, we will create a feature that counts the number of indicators
data['num_indicators'] = data['indicators'].apply(lambda x: len(x.split(',')) if pd.notnull(x) else 0)

# Handle missing values for 'severity' and 'indicators' if any
data.fillna({'severity': 0, 'indicators': ''}, inplace=True)

# Features and target variable
X = data[['severity', 'num_indicators']]  # Add more features as required
y = data['severity']  # Assuming 'severity' is the target variable for prediction

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the model
model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse:.2f}")

# Calculate R² score (Accuracy for regression tasks)
r2 = r2_score(y_test, y_pred)
print(f"R² Score (Accuracy): {r2:.2f}")

# Save the model
joblib.dump(model, 'models/predictive_model.pkl')
print("Model saved successfully.")
