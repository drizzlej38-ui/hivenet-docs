#!/usr/bin/env python3
"""
Analyze stress test results from multiple CSV files
"""

import pandas as pd
import glob
import sys

def analyze_test_file(filepath):
    """Analyze a single test results file"""
    try:
        df = pd.read_csv(filepath)
    except Exception as e:
        print(f"  ❌ Error reading file: {e}")
        return
    
    if len(df) == 0:
        print(f"  ⚠️  No data in file")
        return
    
    # Basic stats
    total = len(df)
    success = (df['status'] == 'completed').sum()
    failed = (df['status'] == 'failed').sum()
    
    print(f"  Total tasks: {total}")
    print(f"  Success: {success} ({success/total*100:.1f}%)")
    print(f"  Failed: {failed} ({failed/total*100:.1f}%)")
    
    # Performance stats from successful tasks
    completed = df[df['status'] == 'completed']
    
    if len(completed) == 0:
        print(f"  ⚠️  No completed tasks to analyze")
        return
    
    print(f"\n  Performance:")
    print(f"    Avg duration: {completed['duration_sec'].mean():.2f}s")
    print(f"    Min duration: {completed['duration_sec'].min():.2f}s")
    print(f"    Max duration: {completed['duration_sec'].max():.2f}s")
    print(f"    Std deviation: {completed['duration_sec'].std():.2f}s")
    
    # Hardware stats
    print(f"\n  Hardware (averages):")
    print(f"    CPU at start: {completed['start_cpu'].mean():.1f}%")
    print(f"    CPU at end: {completed['end_cpu'].mean():.1f}%")
    print(f"    CPU increase: {completed['end_cpu'].mean() - completed['start_cpu'].mean():+.1f}%")
    print(f"    Memory at end: {completed['end_memory'].mean():.1f}%")
    
    # Temperature if available
    if completed['end_temp'].notna().any():
        print(f"    Temperature (avg): {completed['end_temp'].mean():.1f}°C")
        print(f"    Temperature (max): {completed['end_temp'].max():.1f}°C")
        
        if completed['end_temp'].max() > 55:
            print(f"    ⚠️  HIGH TEMPERATURE WARNING")
        elif completed['end_temp'].max() > 45:
            print(f"    ⚠️  Elevated temperature")
    
    # Check for performance degradation
    if len(completed) >= 20:
        first_10 = completed.head(10)['duration_sec'].mean()
        last_10 = completed.tail(10)['duration_sec'].mean()
        change = ((last_10 - first_10) / first_10) * 100
        
        print(f"\n  Stability:")
        print(f"    First 10 tasks avg: {first_10:.2f}s")
        print(f"    Last 10 tasks avg: {last_10:.2f}s")
        print(f"    Change: {change:+.1f}%")
        
        if abs(change) > 20:
            print(f"    ⚠️  SIGNIFICANT DEGRADATION")
        elif abs(change) > 10:
            print(f"    ⚠️  Moderate performance change")
        else:
            print(f"    ✓  Stable performance")
    
    # Memory trend check (for endurance tests)
    if len(completed) >= 50:
        # Compare memory in first quarter vs last quarter
        quarter = len(completed) // 4
        first_quarter_mem = completed.head(quarter)['end_memory'].mean()
        last_quarter_mem = completed.tail(quarter)['end_memory'].mean()
        mem_change = last_quarter_mem - first_quarter_mem
        
        if mem_change > 5:
            print(f"\n  ⚠️  Memory Leak Warning:")
            print(f"    Memory increased by {mem_change:.1f}% over test duration")
        elif mem_change > 2:
            print(f"\n  ⚠️  Slight memory increase: {mem_change:.1f}%")

def main():
    """Analyze all test result files"""
    # Get all CSV files matching test pattern
    files = sorted(glob.glob('test*.csv'))
    
    if not files:
        print("No test result files found (looking for test*.csv)")
        print("Make sure you're in the directory with your test results.")
        sys.exit(1)
    
    print("="*70)
    print("STRESS TEST RESULTS ANALYSIS")
    print("="*70)
    
    for filepath in files:
        print(f"\n📊 {filepath}")
        print("-" * 70)
        analyze_test_file(filepath)
    
    print("\n" + "="*70)
    print("OVERALL RECOMMENDATIONS")
    print("="*70)
    
    # Load all data for cross-test analysis
    all_data = []
    for filepath in files:
        try:
            df = pd.read_csv(filepath)
            df['test_file'] = filepath
            all_data.append(df)
        except:
            continue
    
    if not all_data:
        print("Could not load any test data for overall analysis")
        return
    
    combined = pd.concat(all_data, ignore_index=True)
    completed = combined[combined['status'] == 'completed']
    
    if len(completed) == 0:
        print("No completed tasks to analyze")
        return
    
    # Overall stats
    total_success = len(completed)
    total_tasks = len(combined)
    success_rate = total_success / total_tasks * 100
    
    print(f"\n📈 Aggregate Statistics:")
    print(f"   Total tasks across all tests: {total_tasks}")
    print(f"   Overall success rate: {success_rate:.1f}%")
    print(f"   Average task duration: {completed['duration_sec'].mean():.2f}s")
    
    # Identify issues
    print(f"\n⚠️  Issues Detected:")
    issues_found = False
    
    if success_rate < 95:
        print(f"   • Low success rate ({success_rate:.1f}%) - investigate failures")
        issues_found = True
    
    if completed['end_temp'].notna().any():
        max_temp = completed['end_temp'].max()
        if max_temp > 55:
            print(f"   • High temperature reached ({max_temp:.1f}°C) - thermal management needed")
            issues_found = True
    
    # Check for memory issues
    if len(completed) > 100:
        # Split into thirds
        third = len(completed) // 3
        first_third = completed.head(third)['end_memory'].mean()
        last_third = completed.tail(third)['end_memory'].mean()
        mem_growth = last_third - first_third
        
        if mem_growth > 5:
            print(f"   • Memory growth detected ({mem_growth:.1f}%) - possible memory leak")
            issues_found = True
    
    if not issues_found:
        print(f"   ✓ No major issues detected")
    
    # Recommendations
    print(f"\n💡 Next Steps:")
    
    if success_rate < 95:
        print(f"   1. Improve error handling and retry logic")
    
    if completed['end_temp'].notna().any() and completed['end_temp'].max() > 50:
        print(f"   1. Add thermal management (cooldown periods, lower CPU usage)")
    
    if len(completed) > 100:
        third = len(completed) // 3
        first_third = completed.head(third)['duration_sec'].mean()
        last_third = completed.tail(third)['duration_sec'].mean()
        perf_change = ((last_third - first_third) / first_third) * 100
        
        if perf_change > 15:
            print(f"   2. Investigate performance degradation ({perf_change:+.1f}%)")
    
    if success_rate >= 95 and (not completed['end_temp'].notna().any() or completed['end_temp'].max() < 50):
        print(f"   1. ✓ System stable - ready to scale to multiple nodes")
        print(f"   2. Consider adding task queuing for better load distribution")
        print(f"   3. Implement node health monitoring and auto-scaling")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    main()
