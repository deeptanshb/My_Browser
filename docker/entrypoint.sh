#!/bin/bash
set -e

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║       MY BROWSER  —  Cloud Edition (Docker)         ║"
echo "║       AI + Security Microservices                   ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
echo "  noVNC  →  http://localhost:${NOVNC_PORT:-6080}/vnc.html"
echo "  VNC    →  localhost:${VNC_PORT:-5900}"
echo "  CORS   →  localhost:${CORS_PROXY_PORT:-8081}"
echo ""

mkdir -p /root/.mybrowser/logs
mkdir -p /root/.mybrowser/security
mkdir -p /var/log/supervisor

OLLAMA_HOST="${OLLAMA_HOST:-host.docker.internal}"
OLLAMA_URL="http://${OLLAMA_HOST}:11434"

echo "Checking Ollama at ${OLLAMA_URL} ..."
if curl -sf "${OLLAMA_URL}/api/tags" --max-time 5 > /dev/null 2>&1; then
    echo "Ollama reachable — AI chatbot enabled"
else
    echo "Ollama not reachable at ${OLLAMA_URL} — AI will run in fallback mode"
    echo "To enable AI: make sure the ollama service is running and healthy"
fi

echo ""
echo "Starting all services ..."
echo ""

mkdir -p /root/.fluxbox
cp /app/docker/fluxbox/init /root/.fluxbox/init 2>/dev/null || true
cp /app/docker/fluxbox/apps /root/.fluxbox/apps 2>/dev/null || true

exec /usr/bin/supervisord -c /etc/supervisor/conf.d/mybrowser.conf


