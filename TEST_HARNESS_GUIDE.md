# Test Harness - Stress Testing Guide

## What It Does

The test harness automatically and repeatedly sends tasks to your distributed computing system, logging everything so you can see:

- How nodes handle sustained load
- CPU/memory/temperature changes over time
- Task completion rates
- Any failures or errors
- Hardware performance under stress

## Requirements

```bash
pip install requests
```

## Basic Usage

### 1. Start Your System First

Make sure coordinator and at least one worker are running:

```bash
# Terminal 1 - Tablet
python coordinator.py

# Terminal 2 - Worker device
python worker_node.py <tablet_ip>
```

### 2. Run Continuous Test

**Simple test (runs forever until you press Ctrl+C):**
```bash
python test_harness.py
```

**Run for specific duration (100 tests):**
```bash
python test_harness.py --max 100
```

**Change task complexity:**
```bash
python test_harness.py --task prime_simple    # Easy tasks
python test_harness.py --task prime_standard  # Medium tasks
python test_harness.py --task prime_complex   # Hard tasks
```

**Adjust delay between tests:**
```bash
python test_harness.py --delay 5  # 5 seconds between tests
python test_harness.py --delay 1  # 1 second (more stress)
```

### 3. Run Mixed Workload

Tests with different task types rotating:

```bash
python test_harness.py --mixed --delay 5
```

This cycles through simple → standard → complex tasks.

## What You'll See

```
==============================================================
STARTING CONTINUOUS STRESS TEST
==============================================================
Task type: prime_standard
Delay between tests: 3s
Max tests: unlimited
Log file: test_results.csv

Press Ctrl+C to stop
==============================================================

Found 1 node(s). Starting tests...

============================================================
Test #1 - 14:23:45
Task: prime_standard
✅ SUCCESS - 2.145s on node abc12345
   Results: 1229 items
   CPU: 45.2% | Memory: 52.1% | Temp: 38.5°C

Active nodes: 1
  ✓ Samsung-Tablet (abc12345): ready - 1 tasks
```

## Analyzing Results

All results are logged to `test_results.csv`. You can:

**Open in spreadsheet app** to view/analyze

**Calculate stats with Python:**
```python
import pandas as pd

df = pd.read_csv('test_results.csv')

# Average task duration
print(f"Avg duration: {df['duration_sec'].mean():.2f}s")

# Success rate
success_rate = (df['status'] == 'completed').sum() / len(df) * 100
print(f"Success rate: {success_rate:.1f}%")

# CPU usage trends
print(f"Avg CPU start: {df['start_cpu'].mean():.1f}%")
print(f"Avg CPU end: {df['end_cpu'].mean():.1f}%")

# Temperature (if available)
if df['end_temp'].notna().any():
    print(f"Avg temp: {df['end_temp'].mean():.1f}°C")
    print(f"Max temp: {df['end_temp'].max():.1f}°C")
```

## Stress Testing Scenarios

### Scenario 1: Baseline Performance
**Goal:** See how one node handles steady load

```bash
python test_harness.py --task prime_standard --delay 3 --max 50
```

Run for ~2-3 minutes, check if performance stays consistent.

### Scenario 2: Heavy Load
**Goal:** Push the hardware

```bash
python test_harness.py --task prime_complex --delay 1 --max 100
```

Watch CPU and temperature. Does the device throttle?

### Scenario 3: Endurance Test
**Goal:** Run for hours to check stability

```bash
python test_harness.py --task prime_standard --delay 5
```

Let it run for 30-60 minutes or longer. Any crashes? Memory leaks?

### Scenario 4: Mixed Workload
**Goal:** Test handling of varied task types

```bash
python test_harness.py --mixed --delay 4 --max 150
```

See how the node switches between light and heavy tasks.

## Stopping the Test

Press **Ctrl+C** at any time. The test harness will:
- Stop gracefully
- Show summary statistics
- Keep all logged data

```
============================================================
Shutting down test harness...
Total tests run: 147
Tests failed: 2
Success rate: 98.6%
Results saved to: test_results.csv
============================================================
```

## What to Look For

### Good Signs ✅
- Consistent task completion times
- CPU returns to baseline between tasks
- Temperature stays under ~45°C
- No errors in logs
- Success rate > 95%

### Warning Signs ⚠️
- Completion times increasing over time (may indicate thermal throttling)
- CPU staying at 100%
- Temperature > 50°C
- Increasing error rate
- Memory usage climbing

### Critical Issues 🚨
- Worker crashes
- Tasks timing out
- System becoming unresponsive
- Temperature > 60°C

## Advanced Options

**Custom log file:**
```bash
python test_harness.py --log my_stress_test.csv
```

**Different coordinator URL:**
```bash
python test_harness.py --url http://192.168.1.100:8000
```

**Help:**
```bash
python test_harness.py --help
```

## Next Steps After Testing

Once you've run tests and analyzed results, you'll know:

1. **How long can nodes run continuously?**
2. **What task complexity is sustainable?**
3. **Are there thermal issues?**
4. **Does performance degrade over time?**
5. **What's the failure rate?**

This data tells you what needs improvement: thermal management, task distribution, error handling, etc.
