from flask import Flask, request, jsonify
import time
import random
import json
import os

app = Flask(__name__)

# Directory structure
os.makedirs("result_data", exist_ok=True)
os.makedirs("result_visuals", exist_ok=True)
os.makedirs("logs", exist_ok=True)
os.makedirs("interim_data", exist_ok=True)

# Load dynamically generated resources from a JSON file
RESOURCE_FILE = "interim_data/web_resources.json"

try:
    with open(RESOURCE_FILE, "r") as f:
        web_resources = json.load(f)
except FileNotFoundError:
    print("Warning: web_resources.json not found in interim_data/. Using default resources.")
    web_resources = {
        "/index.html": {"size": 10, "latency": 0.1},
        "/style.css": {"size": 5, "latency": 0.05},
        "/script.js": {"size": 8, "latency": 0.08},
        "/image1.jpg": {"size": 50, "latency": 0.3},
        "/image2.jpg": {"size": 45, "latency": 0.25},
        "/video.mp4": {"size": 200, "latency": 1.0}
    }

@app.route('/<path:resource>', methods=['GET'])
def serve_resource(resource):
    resource_path = f"/{resource}"
    if resource_path in web_resources:
        time.sleep(web_resources[resource_path]["latency"])  # Simulate network delay
        return jsonify({"message": f"Served {resource_path}", "size": web_resources[resource_path]["size"]})
    
    return jsonify({"error": "Resource not found"}), 404  # Return 404 if resource doesn't exist

if __name__ == '__main__':
    # Log output to logs/server_runtime.log
    from werkzeug.serving import WSGIRequestHandler
    import sys

    sys.stdout = open("logs/server_runtime.log", "w")
    sys.stderr = sys.stdout
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run(debug=True)