import pandas as pd
import random

# Load request data
df = pd.read_csv("request_data.csv")

# Generate realistic size and latency dynamically based on resource categories
def assign_size_and_latency(resource):
    if "small_images" in resource:
        size = random.randint(10, 50)  # Small images (KB)
        latency = round(random.uniform(0.05, 0.2), 2)  # Fast retrieval
    elif "large_images" in resource:
        size = random.randint(100, 500)  # Large images (KB)
        latency = round(random.uniform(0.2, 0.5), 2)  # Medium latency
    elif "videos" in resource:
        size = random.randint(1000, 50000)  # Video files (KB)
        latency = round(random.uniform(0.5, 2.0), 2)  # High latency
    elif "scripts" in resource:
        size = random.randint(5, 30)  # JavaScript files (KB)
        latency = round(random.uniform(0.03, 0.1), 2)  # Very fast retrieval
    elif "css" in resource:
        size = random.randint(5, 30)  # CSS files (KB)
        latency = round(random.uniform(0.03, 0.1), 2)  # Very fast retrieval
    else:
        size = random.randint(10, 500)  # Default fallback
        latency = round(random.uniform(0.1, 0.5), 2)  

    return pd.Series([size, latency])

# Apply function to dynamically assign sizes and latencies
df[["size", "latency"]] = df["resource"].apply(assign_size_and_latency)

# Save the updated dataset
df.to_csv("processed_request_data.csv", index=False)
print("Processed dataset saved to processed_request_data.csv")