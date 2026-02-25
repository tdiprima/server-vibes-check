# psutil magic: CPU, RAM, processes – all in one lib
import psutil

def check_cpu_usage(threshold=80):
    usage = psutil.cpu_percent(interval=1)
    return usage > threshold, usage
