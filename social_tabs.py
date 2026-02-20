"""Social Media Quick Access Module"""

class SocialTabManager:
    PLATFORMS = {
        'facebook':  {'name': 'Facebook',  'url': 'https://www.facebook.com',  'icon': '📘'},
        'instagram': {'name': 'Instagram', 'url': 'https://www.instagram.com', 'icon': '📷'},
        'gmail':     {'name': 'Gmail',     'url': 'https://mail.google.com',   'icon': '📧'},
        'telegram':  {'name': 'Telegram',  'url': 'https://web.telegram.org',  'icon': '✈️'},
    }

    def __init__(self, browser):
        self.browser = browser

    def open_platform(self, platform_id):
        """Delegate to browser's _open_social method (uses correct CustomBrowserTab)"""
        self.browser._open_social(platform_id)

    def get_all_platforms(self):
        return self.PLATFORMS