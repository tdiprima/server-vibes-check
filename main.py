# Checks everything, emails if bad. 📋
from loguru import logger
from checks.disk_usage import check_disk_usage
from checks.cpu_usage import check_cpu_usage
from checks.service_status import check_service_status
from actions.restart_service import restart_service
from actions.send_email import send_email
from config import ALERT_EMAIL, CHECKS

def main():
    # Disk Check
    disk_alert, disk_percent = check_disk_usage(CHECKS["disk_usage"]["threshold"])
    logger.info("Disk Usage: {}% (Threshold: {}%)", disk_percent, CHECKS["disk_usage"]["threshold"])
    if disk_alert:
        send_email("Disk Alert", f"Disk usage at {disk_percent}%", ALERT_EMAIL)
        # logger.warning("ALERT: Disk usage exceeds threshold!")

    # CPU Check
    cpu_alert, cpu_percent = check_cpu_usage(CHECKS["cpu_usage"]["threshold"])
    logger.info("CPU Usage: {}% (Threshold: {}%)", cpu_percent, CHECKS["cpu_usage"]["threshold"])
    if cpu_alert:
        send_email("CPU Alert", f"CPU usage at {cpu_percent}%", ALERT_EMAIL)
        # logger.warning("ALERT: CPU usage exceeds threshold!")

    # Service Check
    logger.info("Service Status:")
    for service in CHECKS["services"]:
        down, status = check_service_status(service)
        status_icon = "✓" if not down else "✗"
        logger.info("  {} {}: {}", status_icon, service, status)
        if down:
            logger.warning("Service down: {}. Attempting restart.", service)
            restarted = restart_service(service)
            if restarted:
                logger.info("Service restarted successfully: {}", service)
                restart_note = "Restart attempted: SUCCESS"
            else:
                logger.error("Failed to restart service: {}", service)
                restart_note = "Restart attempted: FAILED"
            send_email(
                f"Service Down: {service}",
                f"Status: {status}\n{restart_note}",
                ALERT_EMAIL,
            )

if __name__ == "__main__":
    main()
