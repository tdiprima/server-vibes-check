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

## Files:
- `systemd/server-vibes-check.service` — oneshot unit, runs main.py once
- `systemd/server-vibes-check.timer` — fires every 15 min (1 min after boot, then every 15 min)
- `env.example` — template for Gmail creds
- `install.sh` — copies to /opt, runs uv sync, installs systemd units, enables timer
- `uninstall.sh` — clean removal (preserves config)

## Usage on server:

```sh
sudo bash install.sh                             # install + enable
sudo vim /etc/server-vibes-check/env             # set Gmail creds
sudo systemctl start server-vibes-check.service  # test run
journalctl -u server-vibes-check -f              # watch logs
```

Now when CPU exceeds the threshold, the email will look something like:

```c
  CPU usage at 92.3%

  Top processes:
    PID   1234   45.2%          root  java
    PID   5678   23.1%        tomcat  python3
    PID    901   12.0%        nobody  ffmpeg
    PID    345    8.4%          root  node
    PID    678    3.6%        deploy  gunicorn
```

### Key points:
  - `get_top_processes()` only runs when the threshold is exceeded, so it doesn't add overhead on normal
  checks
  - Processes with 0% CPU are filtered out to keep the report relevant
  - `NoSuchProcess` and `AccessDenied` are handled since processes can exit between iteration and info lookup

<br>
