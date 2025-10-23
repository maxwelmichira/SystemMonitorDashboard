#!/usr/bin/env python3
import psutil
import subprocess

def get_system_stats():
    # CPU usage (percentage)
    cpu_usage = psutil.cpu_percent(interval=1)
    # Memory usage (total, used, free in MB)
    memory = psutil.virtual_memory()
    mem_total = memory.total / (1024 ** 2)  # Convert bytes to MB
    mem_used = memory.used / (1024 ** 2)
    mem_free = memory.free / (1024 ** 2)
    # CPU temperature (using sensors command)
    cpu_temp = "N/A"
    try:
        temp_output = subprocess.check_output("sensors | grep 'Core 0' | awk '{print $3}'", shell=True).decode().strip()
        cpu_temp = float(temp_output.replace('+', '').replace('°C', ''))
    except Exception as e:
        print(f"Warning: Failed to read temps: {e}")
    # Top 5 memory-hogging processes
    processes = [(p.info['name'], p.info['memory_percent']) for p in psutil.process_iter(['name', 'memory_percent'])]
    top_processes = sorted(processes, key=lambda x: x[1], reverse=True)[:5]

    # Print stats
    print(f"CPU Usage: {cpu_usage}%")
    print(f"Memory: Total={mem_total:.1f}MB, Used={mem_used:.1f}MB, Free={mem_free:.1f}MB")
    print(f"CPU Temp: {cpu_temp}°C")
    print("Top 5 Memory-Hogging Processes:")
    for name, mem_percent in top_processes:
        print(f"  {name}: {mem_percent:.2f}%")

if __name__ == "__main__":
    get_system_stats()
