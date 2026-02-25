# Pings nginx, postgres, etc. Returns if down.
import subprocess

def check_service_status(service_name):
    try:
        output = subprocess.check_output(["systemctl", "is-active", service_name], text=True).strip()
        return output != "active", output
    except subprocess.CalledProcessError:
        return True, "unknown"
