import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Load request data from CSV
df = pd.read_csv("request_data.csv")

# Display the first few rows
print("Dataset Preview:")
print(df.head())

# Display summary statistics
print("\nDataset Info:")
print(df.info())

# Check for missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Handle missing values (if any)
df.dropna(inplace=True)  # Removes rows with missing values

# Ensure "frequency" column is numeric
df["frequency"] = pd.to_numeric(df["frequency"], errors="coerce")

# Save cleaned data
df.to_csv("cleaned_request_data.csv", index=False)
print("Cleaned dataset saved as cleaned_request_data.csv")

# Simulated database of web resources with sizes and latencies
web_resources = {
    "/index.html": {"size": 10, "latency": 0.1},
    "/style.css": {"size": 5, "latency": 0.05},
    "/script.js": {"size": 8, "latency": 0.08},
    "/image1.jpg": {"size": 50, "latency": 0.3},
    "/image2.jpg": {"size": 45, "latency": 0.25},
    "/video.mp4": {"size": 200, "latency": 1.0}
}

# Map size and latency to dataset
df["size"] = df["resource"].map(lambda x: web_resources[x]["size"])
df["latency"] = df["resource"].map(lambda x: web_resources[x]["latency"])

# Save the enriched dataset
df.to_csv("processed_request_data.csv", index=False)
print("Processed dataset saved as processed_request_data.csv")

# Initialize scaler
scaler = MinMaxScaler()

# Normalize frequency and latency
df[["frequency", "latency"]] = scaler.fit_transform(df[["frequency", "latency"]])

# Save the normalized dataset
df.to_csv("normalized_request_data.csv", index=False)
print("Normalized dataset saved as normalized_request_data.csv")