#!/bin/bash
BROWSER_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Starting all services..."

# Tor
sudo systemctl start tor@default

# Ollama (systemd service)
sudo systemctl start ollama-public

# Wait for services
sleep 5

# Docker browser
cd "$BROWSER_DIR"
docker compose down --remove-orphans > /dev/null 2>&1
docker compose up -d

echo ""
echo "✅ All running!"
echo "Open: http://localhost:6080/vnc.html?autoconnect=1&resize=scale"
