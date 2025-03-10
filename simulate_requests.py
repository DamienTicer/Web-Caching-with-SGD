import requests
import random
import time
import pandas as pd

# Base URL of the Flask web server
BASE_URL = "http://127.0.0.1:5000"

# List of available web resources that can be requested
RESOURCES = ["/index.html", "/style.css", "/script.js", "/image1.jpg", "/image2.jpg", "/video.mp4"]

# Dictionary to store the number of times each resource is requested
request_log = {}

# Simulating 1000 requests
for _ in range(100):
    resource = random.choice(RESOURCES)  # Randomly select a resource from the list
    
    try:
        # Send a GET request to the server
        response = requests.get(BASE_URL + resource)
        
        # If the request is successful (status code 200), update the request log
        if response.status_code == 200:
            request_log[resource] = request_log.get(resource, 0) + 1
        else:
            print(f"Warning: {resource} returned status code {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to fetch {resource} - {e}")

    # Add a small delay to simulate real-world user behavior
    time.sleep(random.uniform(0.1, 0.5))  

# Print the request frequency log
print("Request simulation complete. Frequencies:", request_log)

# Convert the request log dictionary into a Pandas DataFrame
df = pd.DataFrame(list(request_log.items()), columns=["resource", "frequency"])

# Save the request frequency data to a CSV file
df.to_csv("request_data.csv", index=False)

print("Request data saved to request_data.csv")