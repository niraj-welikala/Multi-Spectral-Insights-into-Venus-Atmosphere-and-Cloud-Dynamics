import os
from datetime import datetime
import re
from collections import defaultdict

def extract_time_from_lbl(lbl_path):
    """Extract START_TIME from LBL file"""
    try:
        with open(lbl_path, 'r') as f:
            content = f.read()
            
        # Find START_TIME
        time_pattern = r'START_TIME\s*=\s*"([^"]*)"'
        match = re.search(time_pattern, content)
        
        if match:
            time_str = match.group(1)
            # Convert to datetime object
            return datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%f")
        return None
            
    except Exception as e:
        print(f"Error reading {lbl_path}: {e}")
        return None

def analyze_orbit_timing(data_dir):
    """Analyze timing patterns within each orbit"""
    orbit_times = defaultdict(list)
    
    # Walk through the data directory
    for root, dirs, files in os.walk(data_dir):
        # Process only LBL files
        lbl_files = sorted([f for f in files if f.endswith('.LBL')])
        
        if lbl_files:
            orbit = os.path.basename(root)
            
            # Extract times for each LBL file in the orbit
            for lbl_file in lbl_files:
                full_path = os.path.join(root, lbl_file)
                time = extract_time_from_lbl(full_path)
                if time:
                    # Store tuple of (filename, time)
                    orbit_times[orbit].append((lbl_file, time))
    
    # Analyze and print results
    print("\nTiming Analysis by Orbit:")
    print("-" * 50)
    
    for orbit in sorted(orbit_times.keys()):
        times = orbit_times[orbit]
        if len(times) < 2:
            continue
            
        # Sort by time
        times.sort(key=lambda x: x[1])
        
        # Calculate time differences
        time_diffs = []
        for i in range(1, len(times)):
            diff = times[i][1] - times[i-1][1]
            time_diffs.append(diff.total_seconds())
        
        print(f"\nOrbit {orbit}:")
        print(f"Number of observations: {len(times)}")
        print(f"First observation: {times[0][1]}")
        print(f"Last observation: {times[-1][1]}")
        print(f"Total time span: {(times[-1][1] - times[0][1]).total_seconds()/60:.2f} minutes")
        if time_diffs:
            print(f"Average time between observations: {sum(time_diffs)/len(time_diffs)/60:.2f} minutes")
            print(f"Min time between observations: {min(time_diffs)/60:.2f} minutes")
            print(f"Max time between observations: {max(time_diffs)/60:.2f} minutes")

