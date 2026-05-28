# 🦕 DeepBrowse — Privacy Browser with AI & Security

> A custom desktop web browser built in **Python + PyQt6**, Dockerized for cloud deployment via noVNC.
> Features a local AI chatbot (DeepTalks.AI via Ollama), Tor anonymity, real ad/tracker blocking,
> search engine enforcement, IP masking, and a live security dashboard.
> **© Deeptanshu Bhattacharya**

---

## Features

| Feature | Description |
|---------|-------------|
| 🔍 **Multi-Engine Search** | Google, Brave, DuckDuckGo, Yahoo, Bing — enforced via settings |
| 💡 **Search Suggestions** | Real-time autocomplete via DuckDuckGo API |
| 🤖 **DeepTalks.AI** | Local LLM chatbot via Ollama — no cloud, fully private |
| 🧅 **Tor Anonymity** | Route all traffic through Tor — verified anonymous browsing |
| 🚫 **Ad/Tracker Blocking** | Real-time request interception — 20+ blocked domains |
| 🎭 **IP Masking** | 4 algorithms: SHA256 hash, XOR, random subnet, rotate octets |
| 📱 **Social Quick Tabs** | Facebook, Instagram, Gmail, Telegram |
| 🛡️ **Security Dashboard** | Session threat scoring, alert log, block rate, A–F grade |
| 🌐 **Network Monitor** | Per-request logging with allow/block status |
| 🔐 **Privacy Logger** | Local search + page visit logs — never uploaded |
| 📚 **Bookmarks** | Local bookmark management |
| ⬇️ **Download Manager** | Built-in downloads with progress |
| 🧩 **Extensions** | Custom JS/CSS injection per site |
| 💾 **Chat Export** | Save AI conversations to shared folder |
| 🐳 **Docker/Cloud** | Full remote desktop via noVNC — any browser, any OS |

---

## Architecture

```
Your Web Browser (any device, any OS)
        │  HTTP :6080
        ▼
  noVNC web UI (websockify)
        │  WebSocket → VNC :5900
        ▼
  x11vnc ──► Xvfb (virtual display :99)
                     │
                     ▼
            DeepBrowse (PyQt6 + QtWebEngine)
            ├── Network Interceptor (ad blocking)
            ├── IP Masking Monitor
            ├── Social Tab Manager
            └── Security Dashboard
                     │
              CORS Proxy :8081
              ├── /api/*         → Ollama :11434 (AI)
              ├── /search        → DuckDuckGo (web search)
              └── /autocomplete  → DDG suggestions
                     │
              Tor SOCKS5 :9050 (anonymity)
```

---

## Project Structure

```
browser/
├── custom.py                  # Main browser — ModernBrowser(QMainWindow)
├── launch_mybrowser.py        # Startup orchestrator (proxy, deps, Qt init)
├── ollama_cors_proxy.py       # Flask CORS bridge: Ollama + DDG + autocomplete
├── requirements.txt           # Python dependencies
├── install.sh                 # Linux one-click local installer
├── install.bat                # Windows one-click local installer
├── start.sh                   # One-command full-stack launcher
├── Makefile                   # Convenience commands
│
├── modules/                   # Security microservices
│   ├── __init__.py
│   ├── network_interceptor.py # Ad/tracker blocking with live stats
│   ├── ip_masking.py          # IP display masking (4 algorithms)
│   ├── social_tabs.py         # Social media quick-access manager
│   └── security_monitor.py   # Threat scoring & alert dashboard
│
├── docker/                    # Docker support files
│   ├── supervisord.conf       # Process manager (Xvfb→Fluxbox→VNC→noVNC→Browser)
│   ├── entrypoint.sh          # Container startup script
│   ├── maximize.sh            # Window maximize utility
│   └── healthcheck.sh         # Service health checker
│
├── shared/                    # Host ↔ Container file exchange folder
│   ├── uploads/               # Drop files here → available in browser/AI
│   └── exports/               # Exported logs and AI chats appear here
│       └── chats/             # AI conversation exports
│
├── Dockerfile                 # Docker image definition
├── docker-compose.yml         # One-command cloud deployment
└── .dockerignore              # Build context exclusions
```

---

## Quick Start

### Prerequisites

- Ubuntu 22.04 / 24.04
- Docker + Docker Compose v2
- Ollama (for AI chatbot)
- Tor (for anonymous browsing)

### 1 — Install Docker

```bash
curl -fsSL https://get.docker.com | sh
sudo apt install docker-compose-plugin -y
sudo usermod -aG docker $USER && newgrp docker
docker --version && docker compose version
```

### 2 — Install Ollama with auto-start

```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull mistral    # ~4GB recommended model

# Configure to listen on all interfaces (required for Docker)
sudo mkdir -p /etc/systemd/system/ollama.service.d/
sudo tee /etc/systemd/system/ollama.service.d/override.conf << 'EOF'
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
EOF
sudo systemctl daemon-reload
sudo systemctl enable --now ollama
```

### 3 — Install Tor with auto-start

```bash
sudo apt install tor -y

# Configure to listen on all interfaces
echo "SocksPort 0.0.0.0:9050" | sudo tee -a /etc/tor/torrc
sudo systemctl enable --now tor@default

# Verify
ss -tlnp | grep 9050   # should show 0.0.0.0:9050
```

### 4 — Build the browser

```bash
cd ~/Desktop/browser
docker compose build    # First build: ~5 minutes (downloads Ubuntu + PyQt6 + noVNC)
```

---

## Starting All Services

```bash
~/Desktop/browser/start.sh
```

This starts Tor + Docker browser. Ollama starts automatically on boot via systemd.

To stop:
```bash
cd ~/Desktop/browser && docker compose down
```

---

## Accessing the Browser

Open in **any web browser** on any device:

```
http://localhost:6080/vnc.html?autoconnect=1&resize=scale
```

For network/cloud access:
```
http://<machine-ip>:6080/vnc.html?autoconnect=1&resize=scale
```

No installation needed on client — works on Windows, Mac, Linux, Android, iOS.

---

## Feature Guide

### Search Engine

1. Select engine in navbar dropdown (Google / Brave / DuckDuckGo / Yahoo / DeepBrowse)
2. For **DeepBrowse** mode: Privacy → Settings → Search Engine → select backend
3. Type in URL bar or home page — autocomplete suggestions appear after 2 characters
4. Logs show the actual engine used

### Tor Anonymity

**Enable:**
1. Privacy → Privacy Settings
2. Host: `socks5://host.docker.internal` — Port: `9050`
3. Check ✅ Enable Proxy/VPN → Save Settings

**Verify:**
Browse to `https://httpbin.org/ip` — the IP shown will be a Tor exit node, not your real IP.

For full verification: `https://check.torproject.org`

**Notes:**
- Browsing is slower with Tor — traffic routes through 3+ encrypted relays
- Disable proxy for normal speed, enable only when anonymity needed
- AI chatbot queries stay local — they do not go through Tor

### AI Chatbot (DeepTalks.AI)

Click **🦖 deeptalks.ai** button (bottom right).

| Button | Function |
|--------|----------|
| 🆕 New | Clear chat and start fresh |
| 💾 Save | Export chat to `shared/exports/chats/` |
| 🖼️ Image | Attach image for AI to analyze |
| 📎 File | Attach text file for AI to read |
| 🔍 Web search | Toggle DuckDuckGo web context |

Every code block has a **📋 Copy** button.

### Privacy Logging

- View: Privacy → View Search Logs (Searches tab + Page Visits tab)
- Export: click Export → file saved to `~/Desktop/browser/shared/exports/`
- Clear: click Clear Logs

### Ad Blocking

- 20+ tracker domains blocked by default
- Add custom: Security → Network Monitor → Block Domain
- Live stats in Security → Network Monitor

### IP Masking

- Security → IP Masking → select algorithm → Apply
- **Note:** display-layer only — does not route traffic
- Real anonymity: use Tor proxy

### P2P File Transfer

- **Send:** Security → P2P Send File → choose file from `shared/uploads/` → share IP + port 9876
- **Receive:** Security → P2P Receive File → enter sender IP + port → saves to `shared/`

---

## File Sharing with Docker

```
Host: ~/Desktop/browser/shared/
Container: /shared/
```

**Upload files to browser/AI:**
```bash
cp myfile.txt ~/Desktop/browser/shared/uploads/
# Then in browser: AI → 📎 File → opens at /shared/uploads/
```

**Get exported files:**
```bash
ls ~/Desktop/browser/shared/exports/
ls ~/Desktop/browser/shared/exports/chats/
```

Files appear instantly — no `docker cp` needed.

---

## Cloud Deployment

```bash
# On any Ubuntu VPS (AWS, DigitalOcean, GCP, Oracle, etc.)
cd ~/browser
docker compose build
~/browser/start.sh

# Open port 6080 in your cloud firewall/security group
# Access from anywhere:
# http://<vps-ip>:6080/vnc.html?autoconnect=1&resize=scale
```

### Add VNC Password (recommended for public access)

In `docker/supervisord.conf`, add `-passwd YourPassword` to x11vnc command, then rebuild.

---

## Useful Commands

```bash
# View live logs
docker compose logs -f mybrowser

# Check all processes inside container
docker exec mybrowser supervisorctl status

# Full health check
make health

# Shell into container
docker exec -it mybrowser bash

# Restart browser only (no rebuild)
docker compose restart mybrowser

# Stop everything
docker compose down

# Wipe all saved data
docker compose down -v
```

---

## Troubleshooting

### Black screen in noVNC
```bash
Ctrl+Shift+R    # hard refresh in Chrome
docker exec mybrowser supervisorctl status
docker exec mybrowser tail -20 /var/log/supervisor/mybrowser.log
```

### AI says "Limited mode"
```bash
sudo systemctl status ollama
curl http://localhost:11434/api/tags
docker exec mybrowser curl http://host.docker.internal:11434/api/tags
```

### Tor not working
```bash
sudo systemctl status tor@default
ss -tlnp | grep 9050
docker exec mybrowser curl --socks5 host.docker.internal:9050 --max-time 30 https://httpbin.org/ip
```

### Wrong search engine
```bash
docker exec mybrowser python3 -c "
import json; f='/root/.mybrowser/settings.json'
d=json.load(open(f)); d['backend_search_engine']='DuckDuckGo'
json.dump(d,open(f,'w'),indent=2); print('Fixed')
"
docker compose restart mybrowser
```

### Export files not appearing
```bash
docker exec mybrowser ls /shared/exports/
sudo chmod -R 777 ~/Desktop/browser/shared/
```

---

## Ports

| Port | Service | Notes |
|------|---------|-------|
| `6080` | **noVNC web UI** | Main access — open in any browser |
| `5900` | VNC direct | For native VNC clients |
| `8081` | CORS Proxy | Ollama + DuckDuckGo relay |
| `11434` | Ollama | AI model server (host) |
| `9050` | Tor SOCKS5 | Anonymous proxy (host) |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.10+ |
| GUI Framework | PyQt6 + QtWebEngine (Chromium) |
| AI Backend | Ollama (local LLM — Mistral, LLaMA3, etc.) |
| CORS Bridge | Flask + Flask-CORS |
| Anonymity | Tor SOCKS5 proxy |
| Containerisation | Docker + Docker Compose v2 |
| Virtual Display | Xvfb |
| Window Manager | Fluxbox |
| Remote Desktop | x11vnc + noVNC (WebSocket) |
| Process Management | Supervisord |
| Search Backend | DuckDuckGo Instant Answer + Autocomplete API |
| DNS | Cloudflare DoH (1.1.1.1) / Google (8.8.8.8) |

---

*DeepBrowse — Privacy-first browser with local AI, built for cloud deployment.*
*© Deeptanshu Bhattacharya | VIT Chennai | B.Tech ECM 2026*
