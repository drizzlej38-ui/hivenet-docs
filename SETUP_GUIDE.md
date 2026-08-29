# Distributed Computing Demo - Setup Guide

## Reality Check - What This Version IS and IS NOT

**What works (v0.2):**
- ✅ Worker nodes announce themselves to coordinator
- ✅ Coordinator tracks node IPs and status
- ✅ Tasks can be sent from coordinator to workers
- ✅ Workers process tasks and return results
- ✅ Web UI displays nodes and task history
- ✅ Works over local WiFi or device hotspot

**Current limitations:**
- ❌ Single task per worker at a time (blocking)
- ❌ No task queue - only one task dispatched at once
- ❌ No authentication or security
- ❌ No retry logic if task fails
- ❌ No graceful handling of node disconnection
- ❌ LAN-only (no internet routing)
- ❌ JSON framing may break on very large messages
- ❌ Node IDs reset on restart (no persistence)
- ❌ No automated stress testing built-in

**This is a proof of concept.** It proves the core idea works: devices can share compute. Everything else comes later.

## FROZEN MESSAGE PROTOCOL (v0.2)

**DO NOT CHANGE WITHOUT DISCUSSION**

This protocol is now locked. All future changes must maintain backward compatibility.

### Node Announcement (Worker → Coordinator)
```json
{
  "type": "node_announce",
  "node_id": "abc12345",
  "device_name": "MyPhone",
  "platform": "Linux",
  "stats": {
    "cpu_percent": 15.2,
    "memory_percent": 45.0,
    "memory_available": 2048,
    "temperature": 35.5
  }
}
```
- Port: 5000
- Direction: Worker connects to Coordinator
- Format: JSON + newline

### Task Dispatch (Coordinator → Worker)
```json
{
  "type": "prime_simple|prime_standard|prime_complex",
  "id": "task_timestamp"
}
```
- Port: 5001
- Direction: Coordinator connects to Worker
- Format: JSON + newline

### Task Result (Worker → Coordinator)
```json
{
  "task_id": "task_timestamp",
  "node_id": "abc12345",
  "status": "completed|failed",
  "duration": 1.234,
  "result_count": 1229,
  "start_stats": { ... },
  "end_stats": { ... },
  "timestamp": "2026-01-09T12:34:56"
}
```
- Same connection as task dispatch
- Sent immediately after task completion
- Format: JSON + newline

## What You Have

Two Python files:
1. **coordinator.py** - Runs on your tablet (the controller)
2. **worker_node.py** - Runs on other devices (the workers)

## Requirements

You need Python 3 and one additional package on each device:

```bash
pip install psutil
```

Or if that doesn't work:
```bash
pip3 install psutil
```

Or on Termux:
```bash
pkg install python
pip install psutil
```

## Setup Steps

### Step 1: Get Your Tablet's IP Address

On your tablet, find its local IP address:

**On Android (Termux):**
```bash
ifconfig wlan0
```
Look for "inet addr" - it'll be something like `192.168.1.100`

**Or simpler:**
```bash
ip addr show wlan0 | grep inet
```

Write down this IP address!

### Step 2: Start the Coordinator (On Your Tablet)

```bash
cd /path/to/files
python coordinator.py
```

You should see:
```
Coordinator started!
==================================================
Open your browser to: http://localhost:8000
==================================================
```

### Step 3: Open the Web Interface

On your tablet, open a browser and go to:
```
http://localhost:8000
```

You should see the control panel!

### Step 4: Start Worker Nodes (On Other Devices)

On your Tepin phone or mom's device:

```bash
python worker_node.py <TABLET_IP>
```

Replace `<TABLET_IP>` with your tablet's IP from Step 1.

Example:
```bash
python worker_node.py 192.168.1.100
```

The worker should say:
```
Worker node abc123 listening on port 5001
Ready to receive tasks from 192.168.1.100
```

### Step 5: Test It!

1. Look at the web interface on your tablet
2. You should see the worker nodes appear in "Active Nodes"
3. Click one of the task buttons (Simple/Standard/Complex)
4. Watch the task get processed!

## Using Hotspot Mode (No WiFi Network)

If you're camping or don't have a WiFi network:

1. **On your tablet:**
   - Go to Settings > Network > Hotspot
   - Turn on WiFi Hotspot
   - Note the hotspot name and password
   - Find your hotspot IP (usually `192.168.43.1` on Android)

2. **On worker devices:**
   - Connect to your tablet's hotspot
   - Run worker_node.py with your hotspot IP

3. **On your tablet:**
   - Start coordinator.py
   - Open browser to `http://192.168.43.1:8000` (or whatever your hotspot IP is)

## Troubleshooting

**"Connection refused"**
- Make sure coordinator is running first
- Check you're using the right IP address
- Make sure devices are on the same network

**"Module not found: psutil"**
- Install it: `pip install psutil`

**"Permission denied"**
- Try: `python3` instead of `python`
- Or: `chmod +x coordinator.py worker_node.py`

**Worker not appearing**
- Check the IP address is correct
- Make sure port 5000 isn't blocked
- Try restarting the coordinator

## What's Next

Once this works, we can add:
- Better node management
- Task queuing
- Performance graphs
- Bluetooth support
- Auto-discovery
- Security features

But first - let's get this basic version working!
