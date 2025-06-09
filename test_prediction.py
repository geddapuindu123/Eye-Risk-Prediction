import pickle
import pandas as pd

# Load the trained model
model = pickle.load(open('riskmodel.pkl', 'rb'))

# Define the feature names exactly as during training
feature_names = ['Age', 'Gender', 'Blood_Pressure', 'Diabetes', 'Smoking', 'Vision_Blur',
                 'Eye_Pain', 'Frequent_Headaches', 'Screen_Time', 'Family_History',
                 'Night_Vision_Issue', 'Redness_Or_Itching', 'Tears_Or_Dryness']

# Create a DataFrame with your test input data
test_input = pd.DataFrame([[19, 2, 90, 80, 0, 0, 1, 0, 5, 0, 0, 0, 1]], columns=feature_names)

# Predict risk level
prediction = model.predict(test_input)
prediction_proba = model.predict_proba(test_input)[0]

print("Test input data:")
print(test_input)

print("\nModel predicted class:", prediction[0])
print("Prediction probabilities:", prediction_proba)

# Map the prediction number back to risk label for clarity
risk_map = {0: "Low", 1: "Medium", 2: "High"}
print(f"Predicted risk level: {risk_map.get(prediction[0], 'Unknown')}")
