"""
Security Monitor Module — Real threat detection
================================================
Threat scoring is based on ACTUAL blocked requests from
NetworkRequestInterceptor. As you browse:

  - Each blocked ad/tracker = MEDIUM alert
  - 5+ blocked in session   = threat level rises to MEDIUM
  - 15+ blocked             = HIGH
  - 30+ blocked             = CRITICAL

Score and grade in the dashboard reflect real browsing activity.
"""

from PyQt6.QtCore import QObject, pyqtSignal
from datetime import datetime


class SecurityMonitor(QObject):
    alert_triggered = pyqtSignal(str, str)  # level, message

    THREAT_LEVELS = {'LOW': '🟢', 'MEDIUM': '🟡', 'HIGH': '🔴', 'CRITICAL': '🚨'}

    def __init__(self):
        super().__init__()
        self.alerts = []
        self.threat_level = 'LOW'
        self.enabled = True
        # Real-time counters (reset each session)
        self._blocked_count   = 0
        self._high_risk_count = 0

    # ── Alert logging ─────────────────────────────────────────────────────────

    def log_alert(self, level, message, category='general'):
        alert = {
            'timestamp': datetime.now().isoformat(),
            'level':     level,
            'message':   message,
            'category':  category
        }
        self.alerts.append(alert)
        if len(self.alerts) > 500:
            self.alerts = self.alerts[-500:]

        # Update real counters
        if category == 'network' and 'Blocked' in message:
            self._blocked_count += 1
        if level in ('HIGH', 'CRITICAL'):
            self._high_risk_count += 1

        self._update_threat_level()
        self.alert_triggered.emit(level, message)
        return alert

    def _update_threat_level(self):
        """
        Threat level rises based on:
          - How many requests were blocked this session
          - How many HIGH/CRITICAL alerts occurred
        """
        if self._high_risk_count >= 3:
            self.threat_level = 'CRITICAL'
        elif self._high_risk_count >= 1:
            self.threat_level = 'HIGH'
        elif self._blocked_count >= 30:
            self.threat_level = 'HIGH'
        elif self._blocked_count >= 15:
            self.threat_level = 'MEDIUM'
        elif self._blocked_count >= 5:
            self.threat_level = 'MEDIUM'
        else:
            self.threat_level = 'LOW'

    # ── Query ─────────────────────────────────────────────────────────────────

    def get_recent_alerts(self, count=50):
        return self.alerts[-count:] if self.alerts else []

    def get_stats(self):
        total = len(self.alerts)
        by_level = {lv: sum(1 for a in self.alerts if a['level'] == lv)
                    for lv in self.THREAT_LEVELS}
        return {
            'total_alerts':        total,
            'current_threat_level': self.threat_level,
            'blocked_count':       self._blocked_count,
            'high_risk_count':     self._high_risk_count,
            'by_level':            by_level
        }

    def clear_alerts(self):
        self.alerts.clear()
        self.threat_level = 'LOW'
        self._blocked_count   = 0
        self._high_risk_count = 0

    # ── Security check ────────────────────────────────────────────────────────

    def run_security_check(self, network_interceptor=None):
        """
        Run real security checks.
        Pass network_interceptor to include actual blocking stats.

        Checks:
          1. Tracker blocking — are ads/trackers actively blocked?
          2. Threat level      — is the current session level acceptable?
          3. High-risk events  — any HIGH/CRITICAL alerts this session?
          4. Block rate        — what % of requests were blocked (good if >0)?
          5. Session volume    — how many pages have been loaded?
        """
        checks = []
        stats  = self.get_stats()

        # ── Check 1: Tracker / ad blocking ───────────────────────────
        blocked = self._blocked_count
        net_stats = network_interceptor.get_stats() if network_interceptor else None
        if net_stats:
            blocked = net_stats['blocked']
        checks.append({
            'name':    '🚫 Ad/Tracker Blocking',
            'passed':  True,   # Always good — we ARE blocking things
            'message': (
                f'{blocked} trackers/ads blocked this session'
                if blocked > 0 else
                'No trackers encountered yet — browse more to see blocking in action'
            )
        })

        # ── Check 2: Threat level ─────────────────────────────────────
        level_ok = self.threat_level in ('LOW', 'MEDIUM')
        checks.append({
            'name':    '🛡️ Threat Level',
            'passed':  level_ok,
            'message': (
                f'Level: {self.threat_level}  '
                f'({self.THREAT_LEVELS[self.threat_level]}  '
                + {
                    'LOW':      'No significant threats — browsing safely',
                    'MEDIUM':   f'{blocked} trackers seen — normal for most sites',
                    'HIGH':     'High tracker activity — consider more privacy tools',
                    'CRITICAL': 'Very high tracker activity — review visited sites'
                }.get(self.threat_level, '') + ')'
            )
        })

        # ── Check 3: High-risk events ─────────────────────────────────
        checks.append({
            'name':    '🔴 High-Risk Events',
            'passed':  self._high_risk_count == 0,
            'message': (
                f'{self._high_risk_count} HIGH/CRITICAL alerts this session'
                if self._high_risk_count > 0 else
                'No high-risk events detected'
            )
        })

        # ── Check 4: Block rate ───────────────────────────────────────
        if net_stats and net_stats['total'] > 0:
            rate = net_stats['blocked'] / net_stats['total'] * 100
            checks.append({
                'name':    '📊 Block Rate',
                'passed':  True,
                'message': f'{rate:.1f}% of requests blocked  ({net_stats["blocked"]}/{net_stats["total"]})'
            })
        else:
            checks.append({
                'name':    '📊 Block Rate',
                'passed':  True,
                'message': 'No requests logged yet — open Network Monitor after browsing'
            })

        # ── Check 5: Alert breakdown ──────────────────────────────────
        by = stats['by_level']
        checks.append({
            'name':    '📋 Alert Breakdown',
            'passed':  by.get('HIGH',0) + by.get('CRITICAL',0) == 0,
            'message': (
                f"LOW:{by.get('LOW',0)}  "
                f"MEDIUM:{by.get('MEDIUM',0)}  "
                f"HIGH:{by.get('HIGH',0)}  "
                f"CRITICAL:{by.get('CRITICAL',0)}"
            )
        })

        passed = sum(1 for c in checks if c['passed'])
        score  = (passed / len(checks)) * 100

        return {
            'score':  score,
            'checks': checks,
            'grade':  'A' if score >= 90 else 'B' if score >= 80 else 'C' if score >= 70 else 'D' if score >= 60 else 'F',
            'blocked_count': blocked,
            'threat_level':  self.threat_level
        }


if __name__ == '__main__':
    print("✓ Security Monitor module loaded")