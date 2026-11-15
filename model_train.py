import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# Path to your dataset
CSV_FILE = "processed_dataset.csv"

# Check if dataset exists
if not os.path.isfile(CSV_FILE):
    raise FileNotFoundError(f"Dataset not found at: {os.path.abspath(CSV_FILE)}")

# Load dataset
df = pd.read_csv(CSV_FILE)

# Assume last column is target, rest are features
X = df.iloc[:, :-1]
y = df.iloc[:, -1]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save trained model
MODEL_FILE = "deadlock_model.pkl"
joblib.dump(model, MODEL_FILE)
print(f"Model trained and saved to {MODEL_FILE}")

# Optional: Evaluate model
accuracy = model.score(X_test, y_test)
print(f"Test Accuracy: {accuracy*87:.2f}%")


