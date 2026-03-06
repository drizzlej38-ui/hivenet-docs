#!/usr/bin/env python3
"""
HiveNet Workspace/Corkboard Server
Serves the shared passing layer interface
"""

from flask import Flask, render_template, jsonify
import sys

app = Flask(__name__)

@app.route('/')
def index():
    """Serve the main workspace interface"""
    return render_template('workspace.html')

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "operational", "service": "hivenet-workspace"})

if __name__ == '__main__':
    port = 5555  # Default workspace port
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    
    print(f"\n{'='*60}")
    print(f"  HiveNet Workspace Starting")
    print(f"  Port: {port}")
    print(f"  Access: http://localhost:{port}")
    print(f"{'='*60}\n")
    
    app.run(host='0.0.0.0', port=port, debug=True)
