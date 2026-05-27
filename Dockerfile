FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Kolkata
ENV DISPLAY=:99
ENV SCREEN_WIDTH=1280
ENV SCREEN_HEIGHT=800
ENV SCREEN_DEPTH=24
ENV VNC_PORT=5900
ENV NOVNC_PORT=6080
ENV CORS_PROXY_PORT=8081
ENV QTWEBENGINE_DISABLE_SANDBOX=1
ENV QTWEBENGINE_CHROMIUM_FLAGS="--disable-gpu --disable-software-rasterizer --no-sandbox --disable-dev-shm-usage"
ENV QT_OPENGL=software
ENV QT_QPA_PLATFORM=xcb
ENV QT_AUTO_SCREEN_SCALE_FACTOR=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    xvfb \
    x11vnc \
    novnc \
    websockify \
    wmctrl \
    xdotool \
    python3 \
    python3-pip \
    python3-pyqt6 \
    python3-pyqt6.qtwebengine \
    fonts-liberation \
    fonts-noto \
    fonts-noto-color-emoji \
    fonts-noto-cjk \
    fonts-dejavu-core \
    fonts-freefont-ttf \
    supervisor \
    libglib2.0-0 \
    libnss3 \
    libatk-bridge2.0-0 \
    libx11-xcb1 \
    libxcb-dri3-0 \
    libdrm2 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libxkbcommon0 \
    libasound2t64 \
    libxss1 \
    libxtst6 \
    fluxbox \
    curl \
    wget \
    xauth \
    && rm -rf /var/lib/apt/lists/*

RUN fc-cache -fv

RUN pip3 install --break-system-packages \
    flask \
    flask-cors \
    requests

WORKDIR /app
RUN mkdir -p modules logs docker /root/.mybrowser/logs /root/.mybrowser/security

COPY custom.py                       ./
COPY launch_mybrowser.py             ./
COPY ollama_cors_proxy.py            ./
COPY modules/__init__.py             modules/
COPY modules/network_interceptor.py  modules/
COPY modules/ip_masking.py           modules/
COPY modules/social_tabs.py          modules/
COPY modules/security_monitor.py     modules/

COPY docker/supervisord.conf  /etc/supervisor/conf.d/mybrowser.conf
COPY docker/entrypoint.sh     /entrypoint.sh
COPY docker/healthcheck.sh    /app/docker/healthcheck.sh
COPY docker/maximize.sh       /app/docker/maximize.sh
COPY docker/fluxbox/             /app/docker/fluxbox/
RUN chmod +x /entrypoint.sh /app/docker/healthcheck.sh /app/docker/maximize.sh

EXPOSE 6080 5900 8081

ENTRYPOINT ["/entrypoint.sh"]
