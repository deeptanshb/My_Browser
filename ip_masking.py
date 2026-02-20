"""IP Masking Monitor Module"""
from PyQt6.QtCore import QObject, pyqtSignal
import socket
import hashlib
import struct
import random

class IPMaskingMonitor(QObject):
    """Monitor and mask IP addresses"""
    
    ip_changed = pyqtSignal(str, str, str)  # original, masked, algorithm
    
    def __init__(self):
        super().__init__()
        self.original_ip = None
        self.masked_ip = None
        self.current_algorithm = 'simple_hash'
        self.enabled = False
        self.history = []
    
    def get_real_ip(self):
        """Get real external IP address"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    def apply_masking(self, algorithm='simple_hash'):
        """Apply IP masking with specified algorithm"""
        self.original_ip = self.get_real_ip()
        self.current_algorithm = algorithm
        
        if algorithm == 'simple_hash':
            self.masked_ip = self._hash_mask(self.original_ip)
        elif algorithm == 'xor_mask':
            self.masked_ip = self._xor_mask(self.original_ip)
        elif algorithm == 'random_subnet':
            self.masked_ip = self._random_subnet(self.original_ip)
        elif algorithm == 'rotate_octets':
            self.masked_ip = self._rotate_octets(self.original_ip)
        else:
            self.masked_ip = self.original_ip
        
        self.enabled = True
        self._log_change()
        self.ip_changed.emit(self.original_ip, self.masked_ip, algorithm)
        return self.masked_ip
    
    def _hash_mask(self, ip):
        """SHA256 hash-based masking"""
        hash_obj = hashlib.sha256(ip.encode())
        hash_bytes = hash_obj.digest()[:4]
        masked = struct.unpack('!I', hash_bytes)[0]
        return socket.inet_ntoa(struct.pack('!I', masked))
    
    def _xor_mask(self, ip):
        """XOR-based masking"""
        ip_int = struct.unpack('!I', socket.inet_aton(ip))[0]
        masked = ip_int ^ 0x12345678
        return socket.inet_ntoa(struct.pack('!I', masked))
    
    def _random_subnet(self, ip):
        """Keep subnet, randomize host"""
        parts = ip.split('.')
        parts[3] = str(random.randint(1, 254))
        return '.'.join(parts)
    
    def _rotate_octets(self, ip):
        """Rotate octets"""
        parts = ip.split('.')
        return '.'.join([parts[-1]] + parts[:-1])
    
    def _log_change(self):
        """Log IP change"""
        from datetime import datetime
        self.history.append({
            'timestamp': datetime.now().isoformat(),
            'original': self.original_ip,
            'masked': self.masked_ip,
            'algorithm': self.current_algorithm
        })
        if len(self.history) > 100:
            self.history = self.history[-100:]
    
    def disable_masking(self):
        """Disable IP masking"""
        self.enabled = False
        self.masked_ip = self.original_ip
    
    def get_status(self):
        """Get current status"""
        return {
            'enabled': self.enabled,
            'original_ip': self.original_ip or self.get_real_ip(),
            'masked_ip': self.masked_ip,
            'algorithm': self.current_algorithm,
            'history_count': len(self.history)
        }
    
    def get_algorithms(self):
        """Get available algorithms"""
        return ['simple_hash', 'xor_mask', 'random_subnet', 'rotate_octets']

if __name__ == "__main__":
    print("✓ IP Masking module loaded")