import requests
import random
import time
import pandas as pd
import numpy as np
import json
from tqdm import tqdm
import os
import threading
from queue import Queue

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
num_requests_per_client = 25
num_clients = 10
resource_list = list(web_resources.keys())
total_requests = num_requests_per_client * num_clients

zipf_distributions = [
    np.clip(np.random.zipf(1.5, num_requests_per_client), 1, len(resource_list))
    for _ in range(num_clients)
]

# Initialize request log and log file
request_log = {resource: 0 for resource in resource_list}
log_file = open("logs/simulate_requests_log.txt", "w")
progress_bar = tqdm(total=total_requests, desc="Simulating Client Requests")

# Thread-safe queue for logging
log_queue = Queue()

# Define thread function
def client_thread(client_id, zipf_distribution):
    for index in zipf_distribution:
        resource = resource_list[index - 1]
        try:
            response = requests.get(BASE_URL + resource, headers={"X-Client-ID": str(client_id)})
            if response.status_code == 200:
                request_log[resource] += 1
            log_queue.put(f"Client {client_id} Request: {resource}, Status: {response.status_code}\n")
        except requests.exceptions.RequestException as e:
            log_queue.put(f"Client {client_id} Error fetching {resource}: {e}\n")

        progress_bar.update(1)
        time.sleep(random.uniform(0.05, 0.2))

# Launch threads
threads = []
for client_id, zipf_distribution in enumerate(zipf_distributions, start=1):
    t = threading.Thread(target=client_thread, args=(client_id, zipf_distribution))
    t.start()
    threads.append(t)

# Wait for all threads to finish
for t in threads:
    t.join()

# Flush remaining logs
while not log_queue.empty():
    log_file.write(log_queue.get())

log_file.close()
progress_bar.close()

# Save request log to CSV
request_df = pd.DataFrame(list(request_log.items()), columns=["resource", "frequency"])
request_df.to_csv("interim_data/request_data.csv", index=False)
print("Request data saved to interim_data/request_data.csv")