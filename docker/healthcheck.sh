#!/bin/bash
# Run inside container: docker exec mybrowser bash /app/docker/healthcheck.sh

echo ""
echo "=== MY BROWSER — HEALTH CHECK ==="
echo ""

ALL_OK=true

check() {
    local name="$1"
    local cmd="$2"
    if eval "$cmd" > /dev/null 2>&1; then
        echo "  [OK]  $name"
    else
        echo "  [FAIL] $name"
        ALL_OK=false
    fi
}

echo "--- Processes (supervisord) ---"
supervisorctl status 2>/dev/null || echo "  supervisord not responding"
echo ""

echo "--- Service checks ---"
check "Xvfb display :99"        "DISPLAY=:99 xdpyinfo"
check "x11vnc on port 5900"     "ss -tlnp | grep ':5900'"
check "noVNC on port 6080"      "ss -tlnp | grep ':6080'"
check "CORS proxy on port 8081" "curl -sf http://localhost:8081/health"
check "Browser process running" "pgrep -f launch_mybrowser.py"
echo ""

echo "--- Ollama ---"
OLLAMA_HOST="${OLLAMA_HOST:-host.docker.internal}"
if curl -sf "http://${OLLAMA_HOST}:11434/api/tags" --max-time 3 > /dev/null 2>&1; then
    echo "  [OK]  Ollama reachable at ${OLLAMA_HOST}:11434"
    MODELS=$(curl -sf "http://${OLLAMA_HOST}:11434/api/tags" | python3 -c \
        "import sys,json; d=json.load(sys.stdin); [print('        -',m['name']) for m in d.get('models',[])]" 2>/dev/null)
    echo "        Models:"
    echo "$MODELS"
else
    echo "  [WARN] Ollama not reachable — AI in fallback mode"
fi
echo ""

echo "--- Log tails ---"
echo "  mybrowser (last 5 lines):"
tail -5 /var/log/supervisor/mybrowser.log 2>/dev/null | sed 's/^/    /'
echo ""

if $ALL_OK; then
    echo "=== ALL CHECKS PASSED ==="
else
    echo "=== SOME CHECKS FAILED — see above ==="
fi
echo ""
