import pandas as pd

data = pd.read_csv("health_data.csv")
print("🧾 CSV Columns:")
print(data.columns.tolist())
