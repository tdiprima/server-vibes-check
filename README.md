# Server Vibes Check 😎

A lightweight Linux server health monitor that checks disk usage, CPU load, and critical service status every 15 minutes — and emails you when something goes wrong.

## When Your Server Is Quietly On Fire

Production servers fail in slow, boring ways: disk fills up at 3 AM, a service crashes after a routine update, CPU spikes and nobody notices until users complain. By the time you find out, the damage is done. Most monitoring stacks that solve this are heavy, require dedicated infrastructure, and take hours to set up.

## A Systemd Timer That Checks, Alerts, and Self-Heals

`server-vibes-check` runs as a systemd timer — no daemon, no external monitoring service, no cloud dependency. Every 15 minutes it checks three things: disk usage, CPU load, and whether your critical services are active. If a threshold is crossed or a service is down, it sends you an email via Gmail SMTP with the details. If a service is down, it tries to restart it automatically and tells you whether that worked.

The email subject includes your hostname so you always know which machine is alerting. A CPU alert includes a ranked list of the top processes consuming CPU at the time, so you're not left guessing.

## What an Alert Looks Like

```
Subject: [web-prod-01] CPU Alert

Host: web-prod-01

CPU usage at 87.3%

Top processes:
  PID   1234   82.1%          www-data  python3
  PID   5678    4.9%              root  mysqld
  PID   9012    0.8%          www-data  gunicorn
```

A service-down alert looks like:

```
Subject: [web-prod-01] Service Down: apache2

Status: failed
Restart attempted: SUCCESS
```

## Usage

**Prerequisites:** Python 3.11+, [`uv`](https://docs.astral.sh/uv/getting-started/installation/), a Linux system with systemd, and a Gmail account with an [App Password](https://support.google.com/accounts/answer/185833).

**1. Clone the repo**

```bash
git clone https://github.com/yourname/server-vibes-check.git
cd server-vibes-check
```

**2. Set your thresholds and services**

Edit `config.py`:

```python
ALERT_EMAIL = "you@example.com"
CHECKS = {
    "disk_usage": {"threshold": 85},   # alert above 85% disk used
    "cpu_usage":  {"threshold": 75},   # alert above 75% CPU
    "services":   ["apache2", "fail2ban", "ssh"]
}
```

**3. Install**

```bash
sudo bash install.sh
```

The installer copies the project to `/opt/server-vibes-check`, sets up a credentials file at `/etc/server-vibes-check/env` (mode 600, root-only), enables the systemd timer, and starts it immediately.

**4. Add your Gmail credentials**

```bash
sudo nano /etc/server-vibes-check/env
```

```
GMAIL_SENDER=you@gmail.com
GMAIL_APP_PASSWORD=your-16-char-app-password
```

**5. Verify it's running**

```bash
# Check timer schedule
systemctl list-timers server-vibes-check.timer

# Trigger a manual run
sudo systemctl start server-vibes-check.service

# Stream logs
journalctl -u server-vibes-check -f
```

**Uninstall**

```bash
sudo bash uninstall.sh
```

---

Built with [`psutil`](https://psutil.readthedocs.io/), [`loguru`](https://loguru.readthedocs.io/), and standard library `smtplib`. Runs on Ubuntu, RHEL, and Rocky Linux.

<br>
