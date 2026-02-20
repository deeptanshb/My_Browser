"""Network Request Interceptor Module"""
from PyQt6.QtCore import QObject, pyqtSignal
from datetime import datetime
import os
import json

# DEFAULT BLOCKED DOMAINS
DEFAULT_BLOCKED_DOMAINS = {
    'doubleclick.net', 'googleadservices.com', 'googlesyndication.com',
    'google-analytics.com', 'facebook.com/tr', 'connect.facebook.net',
    'ads.yahoo.com', 'advertising.com', 'adserver.com', 'adnxs.com',
    'rubiconproject.com', 'pubmatic.com', 'openx.net', 'criteo.com',
    'outbrain.com', 'taboola.com', 'media.net', 'hotjar.com',
    'mixpanel.com', 'amplitude.com', 'segment.com'
}


class NetworkRequestInterceptor(QObject):
    request_logged = pyqtSignal(str, str, bool)

    def __init__(self):
        super().__init__()
        self.requests = []
        self.enabled = True
        self.user_blocked_domains = self._load_user_domains()
        self.blocked_domains = DEFAULT_BLOCKED_DOMAINS | self.user_blocked_domains

    def _config_path(self):
        d = os.path.join(os.path.expanduser('~'), '.mybrowser', 'security')
        os.makedirs(d, exist_ok=True)
        return os.path.join(d, 'blocked_domains.json')

    def _load_user_domains(self):
        try:
            with open(self._config_path()) as f:
                return set(json.load(f).get('user_blocked', []))
        except:
            return set()

    def _save_user_domains(self):
        try:
            with open(self._config_path(), 'w') as f:
                json.dump({'user_blocked': sorted(self.user_blocked_domains)}, f, indent=2)
        except Exception as e:
            print(f"Warning: could not save blocked domains: {e}")

    def log_request(self, url, method='GET'):
        blocked = self.is_blocked(url)
        self.requests.append({
            'timestamp': datetime.now().isoformat(),
            'url': url, 'method': method, 'blocked': blocked
        })
        if len(self.requests) > 1000:
            self.requests = self.requests[-1000:]
        self.request_logged.emit(url, method, blocked)
        return blocked

    def is_blocked(self, url):
        if not self.enabled:
            return False
        url_lower = url.lower()
        return any(d in url_lower for d in self.blocked_domains)

    def get_recent_requests(self, count=200):
        return self.requests[-count:] if self.requests else []

    def get_stats(self):
        total = len(self.requests)
        blocked = sum(1 for r in self.requests if r['blocked'])
        return {'total': total, 'blocked': blocked, 'allowed': total - blocked}

    def clear_log(self):
        self.requests.clear()

    def add_blocked_domain(self, domain):
        domain = domain.strip().lower()
        if domain:
            self.blocked_domains.add(domain)
            self.user_blocked_domains.add(domain)
            self._save_user_domains()

    def remove_blocked_domain(self, domain):
        domain = domain.strip().lower()
        self.blocked_domains.discard(domain)
        if domain in self.user_blocked_domains:
            self.user_blocked_domains.discard(domain)
            self._save_user_domains()

    def get_all_blocked(self):
        return sorted(self.blocked_domains)

    def is_default_domain(self, domain):
        return domain.lower() in DEFAULT_BLOCKED_DOMAINS

    def is_user_domain(self, domain):
        return domain.lower() in self.user_blocked_domains


if __name__ == '__main__':
    print(f"✓ Network Interceptor loaded")
    print(f"  Default blocked domains: {len(DEFAULT_BLOCKED_DOMAINS)}")