#!/usr/bin/env bash
# Remove server-vibes-check systemd service and installed files.
# Run as root: sudo bash uninstall.sh

set -euo pipefail

check_root() {
    if [[ "${EUID}" -ne 0 ]]; then
        echo "ERROR: must run as root (sudo bash uninstall.sh)" >&2
        exit 1
    fi
}

remove_systemd() {
    echo "Stopping and disabling timer..."
    systemctl stop server-vibes-check.timer 2>/dev/null || true
    systemctl disable server-vibes-check.timer 2>/dev/null || true
    rm -f /etc/systemd/system/server-vibes-check.service
    rm -f /etc/systemd/system/server-vibes-check.timer
    systemctl daemon-reload
}

remove_files() {
    echo "Removing /opt/server-vibes-check..."
    rm -rf /opt/server-vibes-check
}

main() {
    check_root
    remove_systemd
    remove_files
    echo ""
    echo "Uninstalled. Config preserved at /etc/server-vibes-check/env (remove manually if wanted)."
}

main "$@"
