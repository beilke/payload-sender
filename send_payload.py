from flask import Flask, request, render_template, jsonify
import socket
import os
import json

app = Flask(__name__)
UPLOAD_FOLDER = "/uploads"
PAYLOADS_FOLDER = "/payloads"  # Use absolute paths for Docker
CONFIG_FILE = "/config/config.json"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PAYLOADS_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["PAYLOADS_FOLDER"] = PAYLOADS_FOLDER

# Load default IP and Port from config.json
default_config = {"default_ip": "127.0.0.1", "default_port": 5001}

if os.path.exists(CONFIG_FILE):
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
        config.setdefault("default_ip", default_config["default_ip"])
        config.setdefault("default_port", default_config["default_port"])
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in config.json. Using defaults.")
        config = default_config
else:
    print("Warning: config.json not found. Using default values.")
    config = default_config

def list_payloads():
    """List all predefined payload files."""
    return [f for f in os.listdir(PAYLOADS_FOLDER) if os.path.isfile(os.path.join(PAYLOADS_FOLDER, f))]

def send_file(ip, port, file_path):
    """Send file contents over TCP to the given IP and port."""
    try:
        if not os.path.exists(file_path):
            return "File does not exist."

        with open(file_path, "rb") as f:
            file_content = f.read()

        with socket.create_connection((ip, int(port)), timeout=5) as sock:
            sock.sendall(file_content)

        return f"Successfully sent {file_path} to {ip}:{port}"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/")
def index():
    """Render the upload form with available payloads, preloaded IP, and Port values."""
    payload_files = list_payloads()
    return render_template("index.html", 
                           default_ip=config["default_ip"], 
                           default_port=config["default_port"],
                           payload_files=payload_files)

@app.route("/upload", methods=["POST"])
def upload_file():
    """Handle file upload or selection from predefined payloads."""
    ip = request.form.get("ip", config["default_ip"])
    port = request.form.get("port", config["default_port"])
    
    selected_payload = request.form.get("payload_file")
    if selected_payload:
        file_path = os.path.join(PAYLOADS_FOLDER, selected_payload)
        if not os.path.exists(file_path):
            return jsonify({"error": "Selected payload file does not exist"})
    else:
        if "file" not in request.files:
            return jsonify({"error": "No file provided"})
        
        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No file selected"})
        
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)

    result = send_file(ip, port, file_path)
    return jsonify({"message": result})

if __name__ == "__main__":
    import sys
    try:
        app.run(host="0.0.0.0", port=5001, debug=False)  # <-- Run on 0.0.0.0 for Docker
    except Exception as e:
        sys.exit(f"Server failed to start: {str(e)}")
