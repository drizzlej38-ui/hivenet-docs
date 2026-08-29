#!/usr/bin/env python3
"""
Test Harness - Automated Stress Testing
Repeatedly sends tasks to coordinator and logs everything.
"""

import requests
import json
import time
import csv
from datetime import datetime
import signal
import sys

class TestHarness:
    def __init__(self, coordinator_url="http://localhost:8000", log_file="test_results.csv"):
        self.coordinator_url = coordinator_url
        self.log_file = log_file
        self.running = True
        self.tests_run = 0
        self.tests_failed = 0
        
        # Set up signal handler for clean shutdown
        signal.signal(signal.SIGINT, self.shutdown)
        
        # Initialize CSV log
        with open(self.log_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'timestamp',
                'test_number',
                'task_type',
                'node_id',
                'status',
                'duration_sec',
                'result_count',
                'start_cpu',
                'end_cpu',
                'start_memory',
                'end_memory',
                'start_temp',
                'end_temp',
                'error'
            ])
    
    def shutdown(self, signum, frame):
        """Handle Ctrl+C gracefully"""
        print("\n\n" + "="*60)
        print("Shutting down test harness...")
        print(f"Total tests run: {self.tests_run}")
        print(f"Tests failed: {self.tests_failed}")
        print(f"Success rate: {(self.tests_run - self.tests_failed) / max(self.tests_run, 1) * 100:.1f}%")
        print(f"Results saved to: {self.log_file}")
        print("="*60)
        self.running = False
        sys.exit(0)
    
    def get_coordinator_status(self):
        """Get current coordinator status"""
        try:
            response = requests.get(f"{self.coordinator_url}/api/status", timeout=5)
            return response.json()
        except Exception as e:
            print(f"Error getting status: {e}")
            return None
    
    def submit_task(self, task_type):
        """Submit a task to the coordinator"""
        task_data = {
            'type': task_type,
            'id': f"test_{self.tests_run}_{int(time.time())}"
        }
        
        try:
            response = requests.post(
                f"{self.coordinator_url}/api/task",
                json=task_data,
                timeout=60
            )
            return response.json()
        except Exception as e:
            return {'error': str(e), 'status': 'failed'}
    
    def log_result(self, task_type, result):
        """Log test result to CSV"""
        timestamp = datetime.now().isoformat()
        
        # Extract data safely
        node_id = result.get('node_id', 'unknown')
        status = result.get('status', 'failed')
        duration = result.get('duration', 0)
        result_count = result.get('result_count', 0)
        
        start_stats = result.get('start_stats', {})
        end_stats = result.get('end_stats', {})
        
        start_cpu = start_stats.get('cpu_percent', 0)
        end_cpu = end_stats.get('cpu_percent', 0)
        start_memory = start_stats.get('memory_percent', 0)
        end_memory = end_stats.get('memory_percent', 0)
        start_temp = start_stats.get('temperature')
        end_temp = end_stats.get('temperature')
        
        error = result.get('error', '')
        
        with open(self.log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp,
                self.tests_run,
                task_type,
                node_id,
                status,
                duration,
                result_count,
                start_cpu,
                end_cpu,
                start_memory,
                end_memory,
                start_temp,
                end_temp,
                error
            ])
    
    def print_status(self, task_type, result, nodes_status):
        """Print current test status to console"""
        print(f"\n{'='*60}")
        print(f"Test #{self.tests_run} - {datetime.now().strftime('%H:%M:%S')}")
        print(f"Task: {task_type}")
        
        if result.get('status') == 'completed':
            print(f"✅ SUCCESS - {result.get('duration')}s on node {result.get('node_id')}")
            print(f"   Results: {result.get('result_count')} items")
            
            end_stats = result.get('end_stats', {})
            print(f"   CPU: {end_stats.get('cpu_percent', 0):.1f}% | "
                  f"Memory: {end_stats.get('memory_percent', 0):.1f}%", end='')
            if end_stats.get('temperature'):
                print(f" | Temp: {end_stats.get('temperature')}°C")
            else:
                print()
        else:
            print(f"❌ FAILED - {result.get('error', 'Unknown error')}")
            self.tests_failed += 1
        
        # Show node status
        if nodes_status:
            nodes = nodes_status.get('nodes', [])
            print(f"\nActive nodes: {len(nodes)}")
            for node in nodes:
                status_icon = "✓" if node['status'] == 'ready' else "⚠"
                print(f"  {status_icon} {node['device_name']} ({node['node_id']}): "
                      f"{node['status']} - {node['tasks_completed']} tasks")
    
    def run_test_cycle(self, task_type, delay=3):
        """Run one test cycle"""
        self.tests_run += 1
        
        # Submit task
        result = self.submit_task(task_type)
        
        # Get node status
        status = self.get_coordinator_status()
        
        # Log and display
        self.log_result(task_type, result)
        self.print_status(task_type, result, status)
        
        # Wait before next test
        if self.running:
            time.sleep(delay)
    
    def run_continuous(self, task_type='prime_standard', delay=3, max_tests=None):
        """Run continuous stress test"""
        print("="*60)
        print("STARTING CONTINUOUS STRESS TEST")
        print("="*60)
        print(f"Task type: {task_type}")
        print(f"Delay between tests: {delay}s")
        print(f"Max tests: {max_tests if max_tests else 'unlimited'}")
        print(f"Log file: {self.log_file}")
        print("\nPress Ctrl+C to stop")
        print("="*60)
        
        # Wait for nodes to be ready
        print("\nWaiting for nodes to connect...")
        while self.running:
            status = self.get_coordinator_status()
            if status and status.get('nodes'):
                print(f"Found {len(status['nodes'])} node(s). Starting tests...\n")
                break
            time.sleep(2)
        
        # Run tests
        while self.running:
            if max_tests and self.tests_run >= max_tests:
                print(f"\nReached max tests ({max_tests}). Stopping.")
                break
            
            self.run_test_cycle(task_type, delay)
        
        self.shutdown(None, None)
    
    def run_mixed_workload(self, delay=5, max_tests=None):
        """Run mixed workload (simple, standard, complex tasks)"""
        print("="*60)
        print("STARTING MIXED WORKLOAD TEST")
        print("="*60)
        
        task_types = ['prime_simple', 'prime_standard', 'prime_complex']
        task_index = 0
        
        while self.running:
            if max_tests and self.tests_run >= max_tests:
                break
            
            task_type = task_types[task_index % len(task_types)]
            self.run_test_cycle(task_type, delay)
            task_index += 1
        
        self.shutdown(None, None)

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Stress test the distributed computing system')
    parser.add_argument('--url', default='http://localhost:8000', 
                       help='Coordinator URL (default: http://localhost:8000)')
    parser.add_argument('--task', default='prime_standard',
                       choices=['prime_simple', 'prime_standard', 'prime_complex'],
                       help='Task type to run')
    parser.add_argument('--delay', type=int, default=3,
                       help='Delay between tests in seconds (default: 3)')
    parser.add_argument('--max', type=int, default=None,
                       help='Maximum number of tests (default: unlimited)')
    parser.add_argument('--mixed', action='store_true',
                       help='Run mixed workload (cycles through all task types)')
    parser.add_argument('--log', default='test_results.csv',
                       help='Log file path (default: test_results.csv)')
    
    args = parser.parse_args()
    
    harness = TestHarness(coordinator_url=args.url, log_file=args.log)
    
    if args.mixed:
        harness.run_mixed_workload(delay=args.delay, max_tests=args.max)
    else:
        harness.run_continuous(task_type=args.task, delay=args.delay, max_tests=args.max)

if __name__ == "__main__":
    main()
