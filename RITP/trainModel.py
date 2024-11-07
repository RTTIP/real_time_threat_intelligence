import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sqlalchemy import create_engine
import joblib

# Replace with your database connection URL
engine = create_engine('postgresql://postgres:nikhilesh@localhost/asset_management_database')

query = """
SELECT a.asset_id, a.type, a.value, a.criticality, 
       ar.risk_score, ar.threat_level, ar.last_evaluation,
       i.impact_score
FROM assets a
JOIN asset_risks ar ON a.asset_id = ar.asset_id
JOIN incidents i ON a.asset_id = i.asset_id
WHERE i.impact_score IS NOT NULL
"""
data = pd.read_sql(query, engine)

# Convert datetime to numerical value (days since the latest incident evaluation)
data['last_evaluation'] = pd.to_datetime(data['last_evaluation'])
data['days_since_evaluation'] = (pd.to_datetime('now') - data['last_evaluation']).dt.days

# Drop the original datetime column as it's no longer needed
data = data.drop(columns=['last_evaluation'])

# Encode categorical columns
label_encoders = {}
for column in ['type', 'criticality', 'threat_level']:
    le = LabelEncoder()
    data[column] = le.fit_transform(data[column])
    label_encoders[column] = le

# Separate features and target variable
X = data.drop(columns=['impact_score'])
y = data['impact_score']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest Regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the trained model
joblib.dump(model, 'C:/Users/cvnik/Desktop/impact_prediction_model.pkl')
