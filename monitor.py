#!/usr/bin/env python3
import psutil
import subprocess
from flask import Flask, render_template

app = Flask(__name__)

def get_system_stats():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    mem_total = memory.total / (1024 ** 2)
    mem_used = memory.used / (1024 ** 2)
    mem_free = memory.free / (1024 ** 2)
    cpu_temp = "N/A"
    try:
        temp_output = subprocess.check_output("sensors | grep 'Core 0' | awk '{print $3}'", shell=True).decode().strip()
        cpu_temp = float(temp_output.replace('+', '').replace('°C', ''))
    except Exception as e:
        print(f"Warning: Failed to read temps: {e}")
    processes = [(p.info['name'], p.info['memory_percent']) for p in psutil.process_iter(['name', 'memory_percent'])]
    top_processes = sorted(processes, key=lambda x: x[1], reverse=True)[:5]
    return {
        'cpu_usage': cpu_usage,
        'mem_total': mem_total,
        'mem_used': mem_used,
        'mem_free': mem_free,
        'cpu_temp': cpu_temp,
        'top_processes': top_processes
    }

@app.route('/')
def index():
    stats = get_system_stats()
    return render_template('index.html', **stats)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)