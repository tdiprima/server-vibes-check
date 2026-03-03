# Server Vibes Check

I wrote this as a practical way to explore the kind of tooling that keeps a small server healthy without needing a full monitoring stack. The problem I was solving was straightforward but real: I wanted one simple place to check disk usage, CPU pressure, and service health, then raise a flag before a small issue turned into downtime.

## What it does

- **Disk check** — alerts if root partition usage exceeds a configurable threshold (default 85%)
- **CPU check** — alerts if CPU usage exceeds a configurable threshold (default 75%)
- **Service check** — queries `systemctl is-active` for each configured service and alerts if any are down
- **Email alerts** — sends alert emails via Gmail SMTP (currently commented out in `main.py` pending credential setup)
- **Auto-restart** — `actions/restart_service.py` can restart a downed service via `sudo systemctl restart` (not wired into the main loop by default)
- **Scheduler** — `scheduler.py` runs the full check every 15 minutes as a long-running daemon

## Requirements

- Python 3.11+
- Linux with systemd (the service checks use `systemctl`)
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

## Install

```bash
uv sync
```

Or with pip:

```bash
pip install psutil schedule
```

## Configure

Edit `config.py`:

```python
ALERT_EMAIL = "admin@example.com"   # recipient for alerts
CHECKS = {
    "disk_usage": {"threshold": 85},          # percent
    "cpu_usage":  {"threshold": 75},          # percent
    "services":   ["apache2", "nginx", "postgresql"],
}
```

To enable email alerts, fill in your credentials in `actions/send_email.py` and uncomment the `send_email(...)` calls in `main.py`.

## Usage

**Run once:**

```bash
python main.py
```

**Run as a daemon (checks every 15 minutes):**

```bash
python scheduler.py &
```

**Or use cron instead of the scheduler:**

```cron
*/15 * * * * /path/to/venv/bin/python /path/to/server-vibes-check/main.py
```

<br>
