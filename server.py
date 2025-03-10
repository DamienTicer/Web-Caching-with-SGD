# Import necessary Flask modules for building the web server
from flask import Flask, request, jsonify

# Import time module to simulate latency, and random for potential future use
import time
import random

# Create a Flask web application instance
app = Flask(__name__)

# Simulated database of web resources with their size (KB) and latency (seconds)
web_resources = {
    "/index.html": {"size": 10, "latency": 0.1},  # Small HTML file with minimal latency
    "/style.css": {"size": 5, "latency": 0.05},  # Small CSS file with low latency
    "/script.js": {"size": 8, "latency": 0.08},  # JavaScript file with moderate latency
    "/image1.jpg": {"size": 50, "latency": 0.3},  # Large image with higher latency
    "/image2.jpg": {"size": 45, "latency": 0.25},  # Another large image with moderate latency
    "/video.mp4": {"size": 200, "latency": 1.0}  # Large video file with high latency
}

# Define a route that handles GET requests for any resource
@app.route('/<path:resource>', methods=['GET'])
def serve_resource(resource):
    """
    Simulates serving a web resource with a delay based on predefined latency.
    If the resource exists, it returns a JSON response with the resource details.
    If the resource is not found, it returns a 404 error.
    """
    resource_path = f"/{resource}"  # Format resource path to match database keys
    
    # Check if the requested resource exists in the simulated database
    if resource_path in web_resources:
        time.sleep(web_resources[resource_path]["latency"])  # Simulate network delay
        return jsonify({
            "message": f"Served {resource_path}",  # Confirm resource was served
            "size": web_resources[resource_path]["size"]  # Include resource size
        })
    
    # Return a 404 error if the requested resource is not found
    return jsonify({"error": "Resource not found"}), 404

# Start the Flask web server
if __name__ == '__main__':
    app.run(debug=True)  # Enable debug mode for easier debugging and automatic reloads