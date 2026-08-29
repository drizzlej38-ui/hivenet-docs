#!/usr/bin/env python3
"""
Coordinator Node - Distributed Computing Demo
This script runs on your tablet and manages all worker nodes.

PROTOCOL SPECIFICATION:
1. Worker announces to Coordinator on port 5000 (outbound TCP)
2. Coordinator stores worker's IP address from connection
3. Coordinator connects to Worker on port 5001 when sending task
4. Messages are newline-delimited JSON
5. Worker processes task and sends result back on same connection
6. Coordinator receives result and closes connection
"""

import socket
import json
import time
import threading
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse

class Coordinator:
    def __init__(self, port=5000):
        self.port = port
        self.nodes = {}  # Connected worker nodes
        self.task_history = []
        self.running = True
        self.lock = threading.Lock()
        
    def handle_node_announcement(self, data, node_ip):
        """Register a new node or update existing one"""
        with self.lock:
            node_id = data.get('node_id')
            self.nodes[node_id] = {
                'node_id': node_id,
                'node_ip': node_ip,  # CRITICAL: Store the IP address
                'device_name': data.get('device_name'),
                'platform': data.get('platform'),
                'stats': data.get('stats'),
                'status': 'ready',
                'last_seen': datetime.now().isoformat(),
                'tasks_completed': 0
            }
            print(f"Node registered: {node_id} ({data.get('device_name')}) at {node_ip}")
    
    def send_task_to_node(self, node_id, task_data):
        """Send a task to a specific worker node"""
        node = self.nodes.get(node_id)
        if not node:
            return {'error': 'Node not found'}
        
        node_ip = node.get('node_ip')
        if not node_ip:
            return {'error': 'Node IP not available'}
        
        try:
            # Mark node as busy
            with self.lock:
                self.nodes[node_id]['status'] = 'busy'
            
            # Connect to worker node on port 5001
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(30)
            sock.connect((node_ip, 5001))  # CRITICAL: Actually connect!
            
            # Send task
            task_json = json.dumps(task_data).encode() + b'\n'
            sock.sendall(task_json)
            
            print(f"Task sent to node {node_id} at {node_ip}: {task_data.get('type')}")
            
            # Receive result
            result_data = sock.recv(4096).decode()
            result = json.loads(result_data)
            
            sock.close()
            
            # Update node status
            with self.lock:
                self.nodes[node_id]['status'] = 'ready'
                self.nodes[node_id]['tasks_completed'] += 1
                self.task_history.append(result)
            
            return result
            
        except Exception as e:
            with self.lock:
                self.nodes[node_id]['status'] = 'error'
            return {'error': str(e)}
    
    def get_status(self):
        """Get current system status"""
        with self.lock:
            return {
                'nodes': list(self.nodes.values()),
                'task_history': self.task_history[-10:],  # Last 10 tasks
                'timestamp': datetime.now().isoformat()
            }
    
    def listen_for_announcements(self):
        """Listen for worker node announcements"""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('0.0.0.0', self.port))
        server.listen(10)
        server.settimeout(1.0)
        
        print(f"Coordinator listening on port {self.port}")
        
        while self.running:
            try:
                client, addr = server.accept()
                data = client.recv(4096).decode()
                
                if data:
                    msg = json.loads(data)
                    if msg.get('type') == 'node_announce':
                        self.handle_node_announcement(msg, addr[0])  # Pass IP!
                
                client.close()
                
            except socket.timeout:
                continue
            except Exception as e:
                print(f"Error: {e}")
        
        server.close()

class WebHandler(SimpleHTTPRequestHandler):
    """Handle web requests for the UI"""
    coordinator = None
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(get_html_interface().encode())
        
        elif self.path == '/api/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            status = WebHandler.coordinator.get_status()
            self.wfile.write(json.dumps(status).encode())
        
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        """Handle POST requests (task submission)"""
        if self.path == '/api/task':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            task_data = json.loads(post_data.decode())
            
            # Get first available ready node
            ready_nodes = [nid for nid, node in WebHandler.coordinator.nodes.items() 
                          if node.get('status') == 'ready']
            
            if not ready_nodes:
                result = {'error': 'No nodes available'}
            else:
                # Send to first ready node
                node_id = ready_nodes[0]
                result = WebHandler.coordinator.send_task_to_node(node_id, task_data)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
        
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        """Suppress log messages"""
        pass

def get_html_interface():
    """Return HTML for the web interface"""
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Distributed Computing Demo</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #1a1a1a;
            color: #e0e0e0;
        }
        h1 { color: #4CAF50; }
        .section {
            background: #2a2a2a;
            padding: 20px;
            margin: 20px 0;
            border-radius: 8px;
            border: 1px solid #3a3a3a;
        }
        .node {
            background: #333;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            border-left: 4px solid #4CAF50;
        }
        .node.busy { border-left-color: #FFC107; }
        .node.error { border-left-color: #f44336; }
        button {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 12px 24px;
            margin: 5px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
        }
        button:hover { background: #45a049; }
        button:active { background: #3d8b40; }
        .task-history {
            font-family: monospace;
            font-size: 12px;
        }
        .stat { 
            display: inline-block;
            margin-right: 20px;
        }
        .status-ready { color: #4CAF50; }
        .status-busy { color: #FFC107; }
        .status-error { color: #f44336; }
    </style>
</head>
<body>
    <h1>🌐 Distributed Computing Demo</h1>
    
    <div class="section">
        <h2>Active Nodes</h2>
        <div id="nodes">Loading...</div>
    </div>
    
    <div class="section">
        <h2>Submit Task</h2>
        <button onclick="submitTask('prime_simple')">Simple Task (100 primes)</button>
        <button onclick="submitTask('prime_standard')">Standard Task (10K primes)</button>
        <button onclick="submitTask('prime_complex')">Complex Task (100K primes)</button>
    </div>
    
    <div class="section">
        <h2>Task History</h2>
        <div id="history" class="task-history">No tasks yet...</div>
    </div>
    
    <script>
        function updateStatus() {
            fetch('/api/status')
                .then(r => r.json())
                .then(data => {
                    // Update nodes
                    const nodesDiv = document.getElementById('nodes');
                    if (data.nodes.length === 0) {
                        nodesDiv.innerHTML = '<p>No nodes connected yet. Start worker nodes to see them here.</p>';
                    } else {
                        nodesDiv.innerHTML = data.nodes.map(node => `
                            <div class="node ${node.status}">
                                <strong>${node.device_name}</strong> (${node.node_id})
                                <br>
                                <span class="stat">Status: <span class="status-${node.status}">${node.status}</span></span>
                                <span class="stat">Platform: ${node.platform}</span>
                                <span class="stat">Tasks: ${node.tasks_completed}</span>
                                <br>
                                <span class="stat">CPU: ${node.stats.cpu_percent}%</span>
                                <span class="stat">Memory: ${node.stats.memory_percent}%</span>
                                ${node.stats.temperature ? '<span class="stat">Temp: ' + node.stats.temperature + '°C</span>' : ''}
                            </div>
                        `).join('');
                    }
                    
                    // Update history
                    const historyDiv = document.getElementById('history');
                    if (data.task_history.length === 0) {
                        historyDiv.innerHTML = 'No tasks completed yet...';
                    } else {
                        historyDiv.innerHTML = data.task_history.map(task => `
                            <div style="margin: 10px 0; padding: 10px; background: #333; border-radius: 4px;">
                                Task ${task.task_id} on node ${task.node_id}: 
                                ${task.status} in ${task.duration}s 
                                (${task.result_count} results)
                            </div>
                        `).join('');
                    }
                });
        }
        
        function submitTask(taskType) {
            const taskData = {
                type: taskType,
                id: Date.now().toString()
            };
            
            fetch('/api/task', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(taskData)
            })
            .then(r => r.json())
            .then(result => {
                console.log('Task submitted:', result);
                updateStatus();
            });
        }
        
        // Update every 2 seconds
        setInterval(updateStatus, 2000);
        updateStatus();
    </script>
</body>
</html>
"""

def run_coordinator():
    """Main function to run the coordinator"""
    coordinator = Coordinator()
    
    # Set up web handler
    WebHandler.coordinator = coordinator
    
    # Start announcement listener in background thread
    listener_thread = threading.Thread(target=coordinator.listen_for_announcements)
    listener_thread.daemon = True
    listener_thread.start()
    
    # Start web server
    print("\nCoordinator started!")
    print("=" * 50)
    print("Open your browser to: http://localhost:8000")
    print("=" * 50)
    print("\nWaiting for worker nodes to connect...")
    print("(Start worker_node.py on other devices)")
    
    server = HTTPServer(('0.0.0.0', 8000), WebHandler)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down coordinator...")
        coordinator.running = False
        server.shutdown()

if __name__ == "__main__":
    run_coordinator()
