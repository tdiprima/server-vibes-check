# Server Vibes Check

<!--
Lame? Mostly yes — disk check, service status, restart, and scheduling are all trivially doable in    
  bash. The main argument for Python here is psutil for CPU (more reliable than parsing top)
  and structured/testable code. It's not wrong to use Python, just a bit
  heavyweight for what it does.
-->

A Python server monitor. Checks disk usage, CPU load, and systemd service status on a schedule, and sends email alerts when thresholds are exceeded.

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

## Project layout

```
main.py              # orchestrates all checks, prints results, triggers alerts
scheduler.py         # runs main() every 15 minutes using the schedule library
config.py            # thresholds and alert email
checks/
  disk_usage.py      # uses shutil.disk_usage
  cpu_usage.py       # uses psutil.cpu_percent
  service_status.py  # uses systemctl via subprocess
actions/
  send_email.py      # Gmail SMTP alert sender
  restart_service.py # sudo systemctl restart wrapper
```

<br>
