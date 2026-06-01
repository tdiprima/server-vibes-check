# psutil magic: CPU, RAM, processes – all in one lib
import psutil

def get_top_processes(count=5):
    """Return the top CPU-consuming processes as a formatted list."""
    processes = []
    for proc in psutil.process_iter(["pid", "name", "cpu_percent", "username"]):
        try:
            info = proc.info
            if info["cpu_percent"] is not None and info["cpu_percent"] > 0:
                processes.append(info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    processes.sort(key=lambda p: p["cpu_percent"], reverse=True)
    return processes[:count]

def format_top_processes(processes):
    """Format process list into a readable string for alerts."""
    if not processes:
        return "  (no high-CPU processes found)"
    lines = []
    for proc in processes:
        lines.append(
            f"  PID {proc['pid']:>6}  {proc['cpu_percent']:5.1f}%  "
            f"{proc['username'] or 'unknown':>12}  {proc['name']}"
        )
    return "\n".join(lines)

def check_cpu_usage(threshold=80):
    # Prime per-process CPU counters so the second call returns real values
    for proc in psutil.process_iter(["cpu_percent"]):
        pass
    usage = psutil.cpu_percent(interval=1)
    is_alert = usage > threshold
    top_procs = get_top_processes() if is_alert else []
    return is_alert, usage, top_procs
