from flask import Flask, request, jsonify
import time
import random
import json

app = Flask(__name__)

# Load dynamically generated resources from a JSON file
try:
    with open("web_resources.json", "r") as f:
        web_resources = json.load(f)
except FileNotFoundError:
    print("Warning: web_resources.json not found. Using default resources.")
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
    app.run(debug=True)