#!/usr/bin/env bash
# Install server-vibes-check as a systemd timer service.
# Run as root: sudo bash install.sh

set -euo pipefail

INSTALL_DIR="/opt/server-vibes-check"
CONFIG_DIR="/etc/server-vibes-check"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

check_root() {
    if [[ "${EUID}" -ne 0 ]]; then
        echo "ERROR: must run as root (sudo bash install.sh)" >&2
        exit 1
    fi
}

check_uv() {
    if ! command -v uv &>/dev/null; then
        echo "ERROR: uv not found. Install: https://docs.astral.sh/uv/getting-started/installation/" >&2
        exit 1
    fi
}

install_files() {
    echo "Installing to ${INSTALL_DIR}..."
    mkdir -p "${INSTALL_DIR}"
    cp -r "${SCRIPT_DIR}/main.py" \
          "${SCRIPT_DIR}/config.py" \
          "${SCRIPT_DIR}/pyproject.toml" \
          "${SCRIPT_DIR}/checks" \
          "${SCRIPT_DIR}/actions" \
          "${INSTALL_DIR}/"

    if [[ -f "${SCRIPT_DIR}/uv.lock" ]]; then
        cp "${SCRIPT_DIR}/uv.lock" "${INSTALL_DIR}/"
    fi
}

install_deps() {
    echo "Installing Python dependencies..."
    cd "${INSTALL_DIR}"
    uv sync
}

setup_config() {
    if [[ ! -f "${CONFIG_DIR}/env" ]]; then
        echo "Creating config directory..."
        mkdir -p "${CONFIG_DIR}"
        cp "${SCRIPT_DIR}/env.example" "${CONFIG_DIR}/env"
        chmod 600 "${CONFIG_DIR}/env"
        echo ""
        echo "*** IMPORTANT: Edit ${CONFIG_DIR}/env with your Gmail credentials ***"
        echo ""
    else
        echo "Config already exists at ${CONFIG_DIR}/env, skipping."
    fi
}

install_systemd() {
    echo "Installing systemd units..."
    cp "${SCRIPT_DIR}/systemd/server-vibes-check.service" /etc/systemd/system/
    cp "${SCRIPT_DIR}/systemd/server-vibes-check.timer" /etc/systemd/system/
    systemctl daemon-reload
    systemctl enable server-vibes-check.timer
    systemctl start server-vibes-check.timer
}

show_status() {
    echo ""
    echo "Installed. Timer status:"
    systemctl status server-vibes-check.timer --no-pager
    echo ""
    echo "Test manually:  sudo systemctl start server-vibes-check.service"
    echo "View logs:      journalctl -u server-vibes-check -f"
    echo "Check timer:    systemctl list-timers server-vibes-check.timer"
}

main() {
    check_root
    check_uv
    install_files
    install_deps
    setup_config
    install_systemd
    show_status
}

main "$@"
