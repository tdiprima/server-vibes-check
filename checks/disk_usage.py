# Checks root disk, alerts if >90%
import shutil

def check_disk_usage(threshold=90):
    total, used, free = shutil.disk_usage("/")
    percent = used / total * 100
    return percent > threshold, round(percent, 2)
