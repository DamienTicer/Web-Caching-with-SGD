from flask import Flask, request, jsonify
import time
import json
import os

app = Flask(__name__)

# Ensure necessary folders exist
os.makedirs("result_data", exist_ok=True)
os.makedirs("result_visuals", exist_ok=True)
os.makedirs("logs", exist_ok=True)
os.makedirs("interim_data", exist_ok=True)

# Path to dynamic resource file
RESOURCE_FILE = "interim_data/web_resources.json"

# Wait for web_resources.json if it doesn't exist yet
for _ in range(10):
    if os.path.exists(RESOURCE_FILE):
        break
    print("Waiting for web_resources.json...")
    time.sleep(0.5)

@app.route('/<path:resource>', methods=['GET'])
def serve_resource(resource):
    resource_path = f"/{resource}"

    try:
        with open(RESOURCE_FILE, "r") as f:
            web_resources = json.load(f)
    except Exception as e:
        return jsonify({
            "error": "Resource file could not be loaded",
            "details": str(e)
        }), 500

    if resource_path in web_resources:
        time.sleep(web_resources[resource_path]["latency"])  # Simulate network delay
        return jsonify({
            "message": f"Served {resource_path}",
            "size": web_resources[resource_path]["size"]
        })

    return jsonify({"error": "Resource not found"}), 404

if __name__ == '__main__':
    # Log to server_runtime.log
    from werkzeug.serving import WSGIRequestHandler
    import sys

    sys.stdout = open("logs/server_runtime.log", "w")
    sys.stderr = sys.stdout
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run(debug=True)