# Auto-fixes down services. Needs sudo. 🛠️
import subprocess

def restart_service(service_name):
    try:
        subprocess.run(["sudo", "systemctl", "restart", service_name], check=True)
        return True
    except subprocess.CalledProcessError:
        return False
