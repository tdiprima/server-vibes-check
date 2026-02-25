# Change numbers/services here.
ALERT_EMAIL = "admin@example.com"
CHECKS = {
    "disk_usage": {"threshold": 85},
    "cpu_usage": {"threshold": 75},
    "services": ["apache2", "nightwatch-backup.timer"]
}
