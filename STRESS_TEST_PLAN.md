# Systematic Stress Test Plan
## Escalating Load Testing Protocol

This plan systematically tests your nodes from light to heavy load, gathering data at each stage. Run these tests in order.

---

## Test 1: BASELINE - Light Load (15 minutes)
**Goal:** Establish baseline performance under minimal stress

**Command:**
```bash
python test_harness.py --task prime_simple --delay 5 --log test1_baseline.csv
```

**Duration:** 15 minutes (~180 tasks)
**Expected:** Low CPU, stable temps, consistent completion times

**What to watch:**
- Initial CPU/memory/temp readings
- Task duration consistency
- No errors

**Stop after 15 minutes (Ctrl+C)**

---

## Test 2: STANDARD LOAD - Moderate Activity (30 minutes)
**Goal:** See how node handles sustained moderate load

**Command:**
```bash
python test_harness.py --task prime_standard --delay 3 --log test2_standard.csv
```

**Duration:** 30 minutes (~600 tasks)
**Expected:** Moderate CPU (40-60%), temps rise but plateau, stable performance

**What to watch:**
- Does CPU stay consistent or climb?
- Does temperature stabilize or keep rising?
- Task durations: any slowdown over time?

**Stop after 30 minutes (Ctrl+C)**

---

## Test 3: HEAVY LOAD - High Stress (20 minutes)
**Goal:** Push the hardware to see thermal/performance limits

**Command:**
```bash
python test_harness.py --task prime_complex --delay 2 --log test3_heavy.csv
```

**Duration:** 20 minutes (~600 tasks)
**Expected:** High CPU (70-90%), temps may rise significantly, possible throttling

**What to watch:**
- Maximum temperature reached
- CPU throttling (task duration increases)
- Any system instability or crashes
- Does node recover between tasks?

**CRITICAL:** If temp exceeds 60°C or system becomes unstable, stop immediately.

**Stop after 20 minutes (Ctrl+C)**

---

## Test 4: MIXED WORKLOAD - Variable Load (30 minutes)
**Goal:** Test adaptability to changing task complexity

**Command:**
```bash
python test_harness.py --mixed --delay 4 --log test4_mixed.csv
```

**Duration:** 30 minutes (~450 tasks)
**Expected:** CPU/temp fluctuate with task type, no accumulated stress

**What to watch:**
- How quickly node recovers between heavy tasks
- Whether simple tasks complete faster after complex ones (thermal throttling?)
- Overall stability with varying load

**Stop after 30 minutes (Ctrl+C)**

---

## Test 5: RAPID FIRE - Maximum Throughput (10 minutes)
**Goal:** Find the breaking point - how fast can tasks be dispatched?

**Command:**
```bash
python test_harness.py --task prime_standard --delay 1 --log test5_rapid.csv
```

**Duration:** 10 minutes (~600 tasks)
**Expected:** Continuous high load, minimal recovery time, high stress

**What to watch:**
- Task queue buildup (if blocking causes delays)
- Error rate increase
- System responsiveness
- Temperature spike

**CRITICAL:** This is the most stressful test. Monitor closely.

**Stop after 10 minutes (Ctrl+C) or if system becomes unstable**

---

## Test 6: ENDURANCE - Long Duration (2-4 hours)
**Goal:** Detect memory leaks, long-term stability issues, sustained thermal behavior

**Command:**
```bash
python test_harness.py --task prime_standard --delay 5 --log test6_endurance.csv
```

**Duration:** 2-4 hours (1,440 - 2,880 tasks)
**Expected:** Stable long-term operation, no degradation

**What to watch:**
- Memory usage over time (growing = memory leak)
- Task duration drift (getting slower = thermal issue)
- Any crashes or connection losses
- Temperature plateau (should stabilize after ~30 min)

**You can let this run and check on it periodically**

**Stop after 2-4 hours (Ctrl+C)**

---

## Analysis After All Tests

### Quick Analysis Script

Save this as `analyze_results.py`:

```python
import pandas as pd
import glob

# Get all test result files
files = sorted(glob.glob('test*.csv'))

print("="*60)
print("STRESS TEST RESULTS SUMMARY")
print("="*60)

for file in files:
    print(f"\n{file}:")
    df = pd.read_csv(file)
    
    # Basic stats
    total = len(df)
    success = (df['status'] == 'completed').sum()
    failed = (df['status'] == 'failed').sum()
    
    print(f"  Total tasks: {total}")
    print(f"  Success: {success} ({success/total*100:.1f}%)")
    print(f"  Failed: {failed} ({failed/total*100:.1f}%)")
    
    # Performance
    completed = df[df['status'] == 'completed']
    if len(completed) > 0:
        print(f"  Avg duration: {completed['duration_sec'].mean():.2f}s")
        print(f"  Min duration: {completed['duration_sec'].min():.2f}s")
        print(f"  Max duration: {completed['duration_sec'].max():.2f}s")
        
        # Hardware stats
        print(f"  Avg CPU (start): {completed['start_cpu'].mean():.1f}%")
        print(f"  Avg CPU (end): {completed['end_cpu'].mean():.1f}%")
        print(f"  Avg Memory (end): {completed['end_memory'].mean():.1f}%")
        
        # Temperature if available
        if completed['end_temp'].notna().any():
            print(f"  Avg Temp: {completed['end_temp'].mean():.1f}°C")
            print(f"  Max Temp: {completed['end_temp'].max():.1f}°C")
    
    # Check for degradation
    if len(completed) >= 10:
        first_10 = completed.head(10)['duration_sec'].mean()
        last_10 = completed.tail(10)['duration_sec'].mean()
        change = ((last_10 - first_10) / first_10) * 100
        
        if abs(change) > 10:
            print(f"  ⚠️  Performance change: {change:+.1f}% (first 10 vs last 10)")
        else:
            print(f"  ✓  Stable performance ({change:+.1f}% change)")

print("\n" + "="*60)
```

Run after all tests:
```bash
python analyze_results.py
```

---

## Decision Matrix After Testing

Based on test results, decide next priority:

### If you see:
**Thermal issues (temp > 50°C, throttling)**
→ Priority: Thermal management, task scheduling with cool-down periods

**Memory climbing over time**
→ Priority: Fix memory leaks, improve resource cleanup

**High error rate (> 5%)**
→ Priority: Error handling, retry logic, connection stability

**Performance degradation over time**
→ Priority: Investigate throttling, optimize worker code

**All stable, good performance**
→ Priority: Scale to multiple nodes, add task queuing

---

## Timeline

**Day 1 (Today):**
- Tests 1-5 (~2 hours total active testing time)
- Quick analysis between tests

**Day 1-2 (Overnight):**
- Test 6 endurance (let it run while you sleep/do other things)

**Day 2:**
- Analyze all results
- Decide next development priority based on data

---

## Safety Notes

⚠️ **Stop immediately if:**
- Temperature exceeds 60°C
- System becomes unresponsive
- Errors spike above 20%
- Worker crashes repeatedly

✓ **Good practices:**
- Keep devices in open air (not on soft surfaces)
- Monitor first few tests closely
- Have a way to quickly stop everything (Ctrl+C)
- Don't leave devices unattended during heavy load tests

---

## What Success Looks Like

After these tests, you should have:

✅ 6 CSV files with complete performance data
✅ Understanding of your hardware limits
✅ Knowledge of sustained load capacity
✅ Identified any thermal, memory, or stability issues
✅ Confidence in what load your nodes can handle
✅ Data-driven direction for next development phase

This data is GOLD. It tells you exactly what needs improvement.
