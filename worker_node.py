#!/usr/bin/env python3
"""
Worker Node - Distributed Computing Demo
This script runs on devices that will process tasks.

PROTOCOL SPECIFICATION:
1. Worker announces to Coordinator on port 5000 (outbound TCP)
2. Worker listens on port 5001 for incoming task connections
3. Coordinator connects, sends task as newline-delimited JSON
4. Worker processes task and returns result on same connection
5. Connection closes after each task
"""

import socket
import json
import time
import hashlib
import platform
import psutil
from datetime import datetime

class WorkerNode:
    def __init__(self, coordinator_ip, coordinator_port=5000):
        self.coordinator_ip = coordinator_ip
        self.coordinator_port = coordinator_port
        self.node_id = self.generate_node_id()
        self.running = True
        
    def generate_node_id(self):
        """Generate unique node ID based on device info"""
        device_info = f"{platform.node()}-{time.time()}"
        return hashlib.md5(device_info.encode()).hexdigest()[:8]
    
    def get_system_stats(self):
        """Get current system statistics"""
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            
            # Try to get temperature (may not work on all devices)
            temp = None
            try:
                temps = psutil.sensors_temperatures()
                if temps:
                    # Get first available temperature reading
                    temp = list(temps.values())[0][0].current
            except:
                temp = None
            
            return {
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_available': memory.available // (1024 * 1024),  # MB
                'temperature': temp
            }
        except Exception as e:
            return {'error': str(e)}
    
    def calculate_primes(self, limit):
        """Calculate prime numbers up to limit (simple task for testing)"""
        primes = []
        for num in range(2, limit + 1):
            is_prime = True
            for i in range(2, int(num ** 0.5) + 1):
                if num % i == 0:
                    is_prime = False
                    break
            if is_prime:
                primes.append(num)
        return primes
    
    def process_task(self, task_data):
        """Process a task and return results"""
        task_type = task_data.get('type')
        task_id = task_data.get('id')
        
        start_time = time.time()
        start_stats = self.get_system_stats()
        
        result = None
        
        try:
            if task_type == 'prime_simple':
                result = self.calculate_primes(100)
            elif task_type == 'prime_standard':
                result = self.calculate_primes(10000)
            elif task_type == 'prime_complex':
                result = self.calculate_primes(100000)
            else:
                result = {'error': 'Unknown task type'}
            
            duration = time.time() - start_time
            end_stats = self.get_system_stats()
            
            return {
                'task_id': task_id,
                'node_id': self.node_id,
                'status': 'completed',
                'duration': round(duration, 3),
                'result_count': len(result) if isinstance(result, list) else 0,
                'start_stats': start_stats,
                'end_stats': end_stats,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'task_id': task_id,
                'node_id': self.node_id,
                'status': 'failed',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def announce_availability(self):
        """Announce this node to the coordinator"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.coordinator_ip, self.coordinator_port))
            
            announcement = {
                'type': 'node_announce',
                'node_id': self.node_id,
                'device_name': platform.node(),
                'platform': platform.system(),
                'stats': self.get_system_stats()
            }
            
            sock.sendall(json.dumps(announcement).encode() + b'\n')
            sock.close()
            return True
        except Exception as e:
            print(f"Failed to announce: {e}")
            return False
    
    def listen_for_tasks(self):
        """Listen for incoming tasks from coordinator"""
        listen_port = 5001
        
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('0.0.0.0', listen_port))
        server.listen(5)
        server.settimeout(1.0)  # Timeout to allow checking self.running
        
        print(f"Worker node {self.node_id} listening on port {listen_port}")
        print(f"Ready to receive tasks from {self.coordinator_ip}")
        
        while self.running:
            try:
                client, addr = server.accept()
                data = client.recv(4096).decode()
                
                if data:
                    task_data = json.loads(data)
                    print(f"\nReceived task: {task_data.get('type')}")
                    
                    result = self.process_task(task_data)
                    
                    # Send result back
                    client.sendall(json.dumps(result).encode() + b'\n')
                    print(f"Task completed in {result.get('duration')}s")
                
                client.close()
                
            except socket.timeout:
                continue
            except Exception as e:
                print(f"Error: {e}")
        
        server.close()
    
    def run(self):
        """Main run loop"""
        print(f"Starting worker node: {self.node_id}")
        print(f"Device: {platform.node()}")
        print(f"Platform: {platform.system()}")
        
        # Announce to coordinator
        if self.announce_availability():
            print("Successfully announced to coordinator")
        else:
            print("Warning: Could not announce to coordinator")
        
        # Listen for tasks
        try:
            self.listen_for_tasks()
        except KeyboardInterrupt:
            print("\nShutting down worker node...")
            self.running = False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python worker_node.py <coordinator_ip>")
        print("Example: python worker_node.py 192.168.1.100")
        sys.exit(1)
    
    coordinator_ip = sys.argv[1]
    
    node = WorkerNode(coordinator_ip)
    node.run()
