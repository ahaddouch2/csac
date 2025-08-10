from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import json
import os
import shutil
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configuration
RESOURCES_DIR = "ressources"
RESULTS_DIR = "result"

# Ensure directories exist
os.makedirs(RESOURCES_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/config', methods=['GET', 'POST'])
def handle_config():
    config_path = os.path.join(RESOURCES_DIR, 'config.json')
    
    if request.method == 'POST':
        config_data = request.json
        with open(config_path, 'w') as f:
            json.dump(config_data, f, indent=4)
        return jsonify({"message": "Configuration saved successfully"})
    
    try:
        with open(config_path, 'r') as f:
            return jsonify(json.load(f))
    except FileNotFoundError:
        return jsonify({
            "nbProcess": 5,
            "nbMsgs": 10,
            "nbLoops": 1,
            "delay": 2,
            "captcha_api_key": "",
            "sms_api_key": "",
            "sms_service": "Service 1"
        })

@app.route('/api/resource/<filename>', methods=['GET', 'POST'])
def handle_resource(filename):
    filepath = os.path.join(RESOURCES_DIR, filename)
    
    if request.method == 'POST':
        content = request.json.get('content', '')
        with open(filepath, 'w') as f:
            f.write(content)
        return jsonify({"message": f"{filename} saved successfully"})
    
    try:
        with open(filepath, 'r') as f:
            return jsonify({"content": f.read()})
    except FileNotFoundError:
        return jsonify({"content": ""})

@app.route('/api/results', methods=['GET'])
def get_results():
    results = []
    for file in os.listdir(RESULTS_DIR):
        file_path = os.path.join(RESULTS_DIR, file)
        if os.path.isfile(file_path):
            date = datetime.fromtimestamp(os.path.getmtime(file_path))
            results.append({
                "date": date.strftime("%Y-%m-%d %H:%M:%S"),
                "filename": file,
                "status": "Complete"
            })
    return jsonify(results)

@app.route('/api/results/download/<filename>')
def download_result(filename):
    file_path = os.path.join(RESULTS_DIR, filename)
    return send_file(file_path, as_attachment=True)

@app.route('/api/results/clear', methods=['POST'])
def clear_results():
    shutil.rmtree(RESULTS_DIR)
    os.makedirs(RESULTS_DIR)
    return jsonify({"message": "Results cleared successfully"})

@app.route('/api/automation/start', methods=['POST'])
def start_automation():
    actions = request.json.get('actions', [])
    if not actions:
        return jsonify({"error": "No actions selected"}), 400
    # Add your automation logic here
    return jsonify({"message": "Automation started"})

@app.route('/api/automation/pause', methods=['POST'])
def pause_automation():
    # Add your pause logic here
    return jsonify({"message": "Automation paused"})

@app.route('/api/automation/stop', methods=['POST'])
def stop_automation():
    # Add your stop logic here
    return jsonify({"message": "Automation stopped"})

@app.route('/api/automation/kill', methods=['POST'])
def kill_automation():
    # Add your process killing logic here
    return jsonify({"message": "All processes killed"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 