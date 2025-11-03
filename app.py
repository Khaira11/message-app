from flask import Flask, jsonify, request
import os
import json
from datetime import datetime

app = Flask(__name__)

# Message file path - configurable for Docker
MESSAGE_FILE = os.getenv('MESSAGE_FILE_PATH', 'message.txt')

def get_current_message():
    """Read the current message from file"""
    try:
        with open(MESSAGE_FILE, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return "Hello! Webhook test is working! 🚀 Initial deployment."

def update_message(new_message):
    """Update the message in file"""
    with open(MESSAGE_FILE, 'w') as f:
        f.write(new_message)

def get_last_updated():
    """Get last updated timestamp"""
    try:
        timestamp = os.path.getmtime(MESSAGE_FILE)
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    except:
        return 'Never'

@app.route('/')
def home():
    """Main endpoint that shows the current message"""
    message = get_current_message()
    return f"""
    <html>
        <head>
            <title>Webhook Test App</title>
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
                .message {{ background: #f4f4f4; padding: 20px; border-radius: 5px; margin: 20px 0; }}
                .info {{ background: #e7f3ff; padding: 15px; border-radius: 5px; }}
                .container {{ border: 1px solid #ddd; padding: 20px; border-radius: 5px; margin: 10px 0; }}
            </style>
        </head>
        <body>
            <h1>🚀 Webhook Testing App (Docker/K8s)</h1>
            <div class="container">
                <div class="info">
                    <strong>Pod/Container Info:</strong><br>
                    Hostname: {os.getenv('HOSTNAME', 'Unknown')}<br>
                    Environment: {os.getenv('ENVIRONMENT', 'development')}
                </div>
            </div>
            <div class="info">
                <strong>Current Message:</strong>
            </div>
            <div class="message">
                <h2>{message}</h2>
            </div>
            <div class="info">
                <p>To update this message, modify the <code>message.txt</code> file and trigger the webhook.</p>
                <p>Last updated: {get_last_updated()}</p>
                <p>Message file: {MESSAGE_FILE}</p>
            </div>
            <div class="container">
                <h3>API Endpoints:</h3>
                <ul>
                    <li><a href="/api/message">/api/message</a> - Get message as JSON</li>
                    <li><a href="/health">/health</a> - Health check</li>
                </ul>
            </div>
        </body>
    </html>
    """

@app.route('/api/message')
def api_message():
    """API endpoint to get the current message as JSON"""
    return jsonify({
        'message': get_current_message(),
        'status': 'success',
        'timestamp': get_last_updated(),
        'pod': os.getenv('HOSTNAME', 'unknown')
    })

@app.route('/api/update-message', methods=['POST'])
def api_update_message():
    """API endpoint to update the message (for webhook testing)"""
    try:
        data = request.get_json()
        if data and 'message' in data:
            update_message(data['message'])
            return jsonify({
                'status': 'success', 
                'message': 'Message updated successfully',
                'new_message': data['message']
            })
        else:
            return jsonify({'status': 'error', 'message': 'No message provided'}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint for Kubernetes"""
    try:
        get_current_message()  # Test file access
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'pod': os.getenv('HOSTNAME', 'unknown')
        })
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

if __name__ == '__main__':
    # Create initial message file if it doesn't exist
    if not os.path.exists(MESSAGE_FILE):
        update_message("Hello! Webhook test is working! 🚀 Third time deployment.")
    
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
