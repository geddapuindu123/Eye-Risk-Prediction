import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import pickle
import matplotlib.pyplot as plt

# ============================
# 1. Load and Prepare Dataset
# ============================
try:
    data = pd.read_csv("eye_health_risk_dataset_10000.csv")
    print("📂 Dataset loaded successfully.")
except Exception as e:
    raise FileNotFoundError(f"❌ Failed to load dataset: {e}")

print("\n🧾 CSV Columns:")
print(data.columns.tolist())

if data.isnull().sum().any():
    print("⚠️ Missing values found. Filling with column medians.")
    data.fillna(data.median(numeric_only=True), inplace=True)
else:
    print("✅ No missing values detected.")

# ===================
# 2. Define Features
# ===================
feature_columns = [
    'age', 'eye_pressure', 'vision_clarity', 'retina_thickness', 'cornea_health',
    'blood_pressure', 'blood_sugar', 'cholesterol', 'screen_time', 'sleep_hours'
]

target_column = 'risk_level'

try:
    X = data[feature_columns]
    y = data[target_column]
    print("✅ Feature and target columns loaded.")
except KeyError as ke:
    raise KeyError(f"❌ Missing expected column: {ke}")

# =====================
# 3. Train-Test Split
# =====================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print("📊 Data split into training and test sets.")

# =====================
# 4. Train Classifier
# =====================
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight='balanced'
)
model.fit(X_train, y_train)
print("✅ Model training complete.")

# =====================
# 5. Evaluate Model
# =====================
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"\n✅ Accuracy: {accuracy:.2f}")

print("\n📊 Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\n🧾 Classification Report:")
print(classification_report(y_test, y_pred))

# ===============================
# 6. Feature Importance + Plot
# ===============================
importance_df = pd.DataFrame({
    'Feature': feature_columns,
    'Importance': model.feature_importances_
}).sort_values(by='Importance', ascending=False)

print("\n📈 Feature Importance:")
print(importance_df.to_string(index=False))

try:
    importance_df.plot(kind='barh', x='Feature', y='Importance', legend=False, figsize=(8, 6), color='#38b2ac')
    plt.title("🔍 Feature Importance (Random Forest)")
    plt.xlabel("Importance Score")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig("feature_importance_plot.png")
    plt.close()
    print("📊 Feature importance plot saved as 'feature_importance_plot.png'")
except Exception as e:
    print(f"⚠️ Could not generate plot: {e}")

# ===================
# 7. Save the Model
# ===================
try:
    with open('riskmodel.pkl', 'wb') as f:
        pickle.dump(model, f)
    print("💾 Model saved successfully as 'riskmodel.pkl'")
except Exception as e:
    print(f"❌ Failed to save model: {e}")
