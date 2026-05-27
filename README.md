# 🦕 My Browser — Privacy Desktop Browser with AI & Security

> A fully custom desktop web browser built in **Python + PyQt6**, featuring a local AI chatbot (via Ollama), real-time ad/tracker blocking, IP masking, social media quick tabs, and a live security dashboard.  
> Can be run **locally** or **deployed to any cloud server** via Docker — accessible from any web browser through noVNC.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Local Setup (No Docker)](#local-setup-no-docker)
- [Docker Setup (Cloud / Remote Access)](#docker-setup-cloud--remote-access)
- [AI Chatbot (Ollama)](#ai-chatbot-ollama)
- [Module Reference](#module-reference)
- [Ports & Services](#ports--services)
- [Cloud Deployment](#cloud-deployment)
- [Troubleshooting](#troubleshooting)

---

## Features

| Feature | Description |
|---------|-------------|
| 🔍 **Multi-Engine Search** | Google, Brave, DuckDuckGo, Bing, Yahoo, custom home |
| 🤖 **AI Chatbot (DeepTalks.AI)** | Local LLM via Ollama — no data sent to cloud |
| 🚫 **Ad / Tracker Blocking** | Real-time request interception with live block counter |
| 🎭 **IP Masking** | 4 algorithms: SHA256 hash, XOR, random subnet, octet rotation |
| 📱 **Social Tabs** | Quick-access to Facebook, Instagram, Gmail, Telegram |
| 🛡️ **Security Dashboard** | Session threat scoring, alert log, block rate, grade A–F |
| 🌐 **Network Monitor** | Per-request logging with allow/block status |
| 🔐 **Privacy Logger** | Browsing history stored locally, never uploaded |
| 📚 **Bookmarks** | Local bookmark management |
| ⬇️ **Download Manager** | Built-in downloads with progress tracking |
| 🧩 **Extension System** | Custom JS/CSS injection per site |
| 🔌 **VPN Proxy Support** | HTTP/SOCKS5 proxy configuration |
| 🐳 **Docker / Cloud** | Full remote desktop access via noVNC |

---

## Project Structure

```
browser/
├── custom.py                  # Main browser — ModernBrowser(QMainWindow)
├── launch_mybrowser.py        # Startup orchestrator (checks deps, starts services)
├── ollama_cors_proxy.py       # Flask CORS bridge: Ollama AI + DuckDuckGo search
├── requirements.txt           # Python dependencies
├── install.sh                 # Linux one-click installer (local, no Docker)
├── install.bat                # Windows one-click installer (local, no Docker)
├── LICENSE                    # License file
│
├── modules/                   # Security microservices
│   ├── __init__.py
│   ├── network_interceptor.py # Ad/tracker blocking with live stats
│   ├── ip_masking.py          # IP display masking (4 algorithms)
│   ├── social_tabs.py         # Social media quick-access manager
│   └── security_monitor.py   # Threat scoring & alert dashboard
│
├── docker/                    # Docker support files
│   ├── supervisord.conf       # Process manager: Xvfb → VNC → noVNC → Browser
│   └── entrypoint.sh          # Container startup script
│
├── Dockerfile                 # Docker image definition
├── docker-compose.yml         # One-command cloud deployment
├── .dockerignore              # Build context exclusions
├── README.md                  # This file
│
├── screenshots/               # App screenshots
└── myenv/                     # Local Python venv (not used in Docker)
```

---

## Local Setup (No Docker)

### Prerequisites

- Ubuntu 22.04 / 24.04 (or Windows 10/11)
- Python 3.10+
- Ollama (optional, for AI chatbot)

### Linux — Quick Install

```bash
cd ~/Desktop/browser
chmod +x install.sh
./install.sh
```

Or manually:

```bash
# Install PyQt6
sudo apt install python3-pyqt6 python3-pyqt6.qtwebengine -y

# Install Python dependencies
pip3 install flask flask-cors requests --break-system-packages

# Run
python3 launch_mybrowser.py
```

### Windows — Quick Install

```cmd
install.bat
```

Or manually:
```cmd
pip install PyQt6 PyQt6-WebEngine flask flask-cors requests
python launch_mybrowser.py
```

---

## Docker Setup (Cloud / Remote Access)

Docker lets you run the browser on any server and access it from any web browser — no installation needed on the client side.

### How it works

```
Your Web Browser (any device)
        │  HTTP :6080
        ▼
  noVNC web UI
        │  WebSocket → VNC :5900
        ▼
  x11vnc  ──►  Xvfb (virtual display :99)
                      │
                      ▼
             My Browser (PyQt6 GUI)
             ├── Network Interceptor
             ├── IP Masking Monitor
             ├── Social Tab Manager
             └── Security Dashboard
                      │
               CORS Proxy :8081
                      │
               Ollama :11434 (AI)
```

### Step 1 — Verify Docker

```bash
docker --version          # Docker version 29.x.x
docker compose version    # Docker Compose version v2.x.x
```

### Step 2 — Configure for Ollama (only change needed)

If Ollama is running on your **host machine**, edit `docker-compose.yml` under the `mybrowser:` service:

```yaml
mybrowser:
  environment:
    - SCREEN_WIDTH=1280
    - SCREEN_HEIGHT=800
    - SCREEN_DEPTH=24
    - NOVNC_PORT=6080
    - VNC_PORT=5900
    - CORS_PROXY_PORT=8081
    - OLLAMA_HOST=host.docker.internal    # ← change this line
  extra_hosts:
    - "host.docker.internal:host-gateway"  # ← add this block
```

**This is the ONLY change needed.** Everything else is already correct.

### Step 3 — Build

```bash
cd ~/Desktop/browser
docker compose build
```

First build takes **3–5 minutes**. Subsequent builds are cached and fast.

### Step 4 — Run

```bash
# Foreground (see all logs)
docker compose up

# Background
docker compose up -d
```

### Step 5 — Open in browser

```
http://localhost:6080/vnc.html
```

Click **Connect** — the full browser desktop appears in your web browser.

### Useful Docker commands

```bash
# View live logs
docker compose logs -f mybrowser

# Check all running processes inside container
docker exec mybrowser supervisorctl status

# Restart browser without rebuilding
docker compose restart mybrowser

# Open a shell inside the container
docker exec -it mybrowser bash

# Stop everything
docker compose down

# Stop and wipe saved data
docker compose down -v
```

---

## AI Chatbot (Ollama)

The browser includes **DeepTalks.AI** — a built-in AI chatbot powered by a local Ollama LLM. No data leaves your machine.

### Install Ollama on host

```bash
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a model
ollama pull mistral        # ~4GB, good balance
ollama pull llama3.2       # smaller, faster

# Start
ollama serve
```

Then apply the `docker-compose.yml` change from Step 2 above.

### Ollama inside Docker (alternative)

Uncomment the `ollama:` service block in `docker-compose.yml`, then:

```bash
docker compose up --build
docker exec -it ollama ollama pull mistral
```

### No AI (browser-only)

Leave everything as-is. The browser works fully; the chatbot shows a fallback message.

---

## Module Reference

### `custom.py` — Main Browser
Core application. `ModernBrowser(QMainWindow)` with tab management, search engines, privacy logging, bookmarks, downloads, extension system, proxy config, and full microservice integration.

### `launch_mybrowser.py` — Launcher
Startup orchestrator: checks dependencies, detects Ollama, starts CORS proxy, initialises Qt application, handles cleanup on exit.

### `ollama_cors_proxy.py` — CORS Bridge
Flask server on `:8081`. Solves null-origin CORS for the home page loaded via `setHtml()`.
- `/api/*` → Ollama at `:11434`
- `/search?q=` → DuckDuckGo Instant Answer API
- `/health` → status check

### `modules/network_interceptor.py`
Default blocklist of 20+ ad/tracker domains. User-extensible, persisted to `~/.mybrowser/security/blocked_domains.json`. Emits PyQt signals for live UI updates.

### `modules/security_monitor.py`
Session threat scoring: `LOW → MEDIUM → HIGH → CRITICAL` based on blocked request count. Runs a 5-check security audit and assigns a grade A–F.

### `modules/ip_masking.py`
Display-layer IP obfuscation (does not route traffic). Algorithms: `simple_hash`, `xor_mask`, `random_subnet`, `rotate_octets`.

### `modules/social_tabs.py`
Quick-launch tabs for Facebook, Instagram, Gmail, Telegram.

---

## Ports & Services

| Port | Service | Notes |
|------|---------|-------|
| `6080` | **noVNC web UI** | Open this in your browser |
| `5900` | VNC direct | For native VNC clients |
| `8081` | CORS Proxy | Ollama + DuckDuckGo relay |
| `11434` | Ollama | Only if running Ollama in Docker |

---

## Cloud Deployment

```bash
# 1. Open port 6080 in your cloud provider's firewall

# 2. SSH into your VM, transfer the project, then:
docker compose up -d

# 3. Access from anywhere:
http://<your-vm-public-ip>:6080/vnc.html
```

### Add VNC password (recommended for public access)

In `docker/supervisord.conf`, change the x11vnc command:

```ini
command=x11vnc -display :99 -passwd YourSecurePassword -listen 0.0.0.0 -xkb -ncache 10 -ncache_cr -forever -shared
```

Rebuild: `docker compose up --build`

### Persist data

Browser data is saved in a named Docker volume automatically. To back up:

```bash
docker run --rm \
  -v browser_mybrowser_data:/data \
  -v $(pwd):/backup \
  ubuntu tar czf /backup/mybrowser_backup.tar.gz /data
```

---

## Troubleshooting

### Blank screen in noVNC
```bash
docker exec mybrowser supervisorctl status
docker exec mybrowser cat /var/log/supervisor/mybrowser.log
```

### AI not responding
```bash
curl http://localhost:8081/health
docker exec mybrowser curl http://host.docker.internal:11434/api/tags
```

### PyQt6 errors on local run
```bash
sudo apt install python3-pyqt6 python3-pyqt6.qtwebengine -y
```

### Build fails — no space left
```bash
docker system prune -a
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.10+ |
| GUI Framework | PyQt6 + QtWebEngine (Chromium) |
| AI Backend | Ollama (local LLM) |
| CORS Bridge | Flask + Flask-CORS |
| Containerisation | Docker + Docker Compose |
| Virtual Display | Xvfb |
| Remote Desktop | x11vnc + noVNC |
| Process Management | Supervisord |
| Search Backend | DuckDuckGo Instant Answer API |

---

## License

See [LICENSE](LICENSE) for terms.
