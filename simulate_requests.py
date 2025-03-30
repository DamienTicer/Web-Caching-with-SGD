import requests
import random
import time
import pandas as pd
import numpy as np
import json
from tqdm import tqdm
import os

# Create required folders
os.makedirs("interim_data", exist_ok=True)
os.makedirs("logs", exist_ok=True)

# Base URL of the Flask web server
BASE_URL = "http://127.0.0.1:5000"

# Generate a larger set of web resources with varied sizes
categories = {
    "small_images": {"count": 30, "size_range": (10, 50)},  # KB
    "large_images": {"count": 20, "size_range": (100, 500)},  # KB
    "videos": {"count": 10, "size_range": (1000, 50000)},  # KB
    "scripts": {"count": 20, "size_range": (5, 30)},  # KB
    "css": {"count": 20, "size_range": (5, 30)},  # KB
}

web_resources = {}  # Initialize global dictionary

# Generate resource names and sizes
resource_index = 1
for category, properties in categories.items():
    for _ in range(properties["count"]):
        size = random.randint(*properties["size_range"])  # Assign a random size
        latency = random.uniform(0.05, 1.5)  # Assign a random latency between 50ms-1.5s
        resource_name = f"{category}_{resource_index}.dat"  # Unique filename
        web_resources[f"/{resource_name}"] = {"size": size, "latency": latency}
        resource_index += 1

# Save dynamically generated resources so the Flask server can load them
with open("interim_data/web_resources.json", "w") as f:
    json.dump(web_resources, f, indent=4)

print("Web resources saved to interim_data/web_resources.json")

# Simulating request frequencies using a Zipfian (long-tail) distribution
num_requests = 100  # Total simulated requests
resource_list = list(web_resources.keys())

# Generate skewed request frequencies
zipf_distribution = np.random.zipf(1.5, num_requests)
zipf_distribution = np.clip(zipf_distribution, 1, len(resource_list))  # Limit to valid indexes

# Dictionary to track requests
request_log = {resource: 0 for resource in resource_list}

# Open log file
log_file = open("logs/simulate_requests_log.txt", "w")

# Generate requests based on skewed distribution with progress bar
for index in tqdm(zipf_distribution, desc="Processing Requests"):
    resource = resource_list[index - 1]
    try:
        response = requests.get(BASE_URL + resource)  # Simulate request
        if response.status_code == 200:
            request_log[resource] += 1
        log_file.write(f"Request: {resource}, Status: {response.status_code}\n")
    except requests.exceptions.RequestException as e:
        log_file.write(f"Error fetching {resource}: {e}\n")

    time.sleep(random.uniform(0.1, 0.5))  # Random delay

# Save request log to CSV
df = pd.DataFrame(list(request_log.items()), columns=["resource", "frequency"])
df.to_csv("interim_data/request_data.csv", index=False)
print("Request data saved to interim_data/request_data.csv")

log_file.close()