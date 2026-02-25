# Checks everything, emails if bad. 📋
from checks.disk_usage import check_disk_usage
from checks.cpu_usage import check_cpu_usage
from checks.service_status import check_service_status
from actions.send_email import send_email
from config import ALERT_EMAIL, CHECKS

def main():
    # Disk Check
    disk_alert, disk_percent = check_disk_usage(CHECKS["disk_usage"]["threshold"])
    print(f"Disk Usage: {disk_percent}% (Threshold: {CHECKS['disk_usage']['threshold']}%)")
    if disk_alert:
        # send_email("Disk Alert", f"Disk usage at {disk_percent}%", ALERT_EMAIL)
        print("  ⚠️  ALERT: Disk usage exceeds threshold!")

    # CPU Check
    cpu_alert, cpu_percent = check_cpu_usage(CHECKS["cpu_usage"]["threshold"])
    print(f"CPU Usage: {cpu_percent}% (Threshold: {CHECKS['cpu_usage']['threshold']}%)")
    if cpu_alert:
        # send_email("CPU Alert", f"CPU usage at {cpu_percent}%", ALERT_EMAIL)
        print("  ⚠️  ALERT: CPU usage exceeds threshold!")

    # Service Check
    print(f"\nService Status:")
    for service in CHECKS["services"]:
        down, status = check_service_status(service)
        status_icon = "✓" if not down else "✗"
        print(f"  {status_icon} {service}: {status}")
        if down:
            # send_email(f"Service Down: {service}", f"Status: {status}", ALERT_EMAIL)
            print(f"    ⚠️  ALERT: Service is down!")

if __name__ == "__main__":
    main()
