import os
import json

class ConfigReader:
    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

    def get(self, key, default=None):
        return self.config.get(key, default)

    def get_platform_capabilities(self, platform):
        caps = self.config.get("CAPABILITIES", {})
        if platform not in caps:
            raise ValueError(f"Platform '{platform}' not found in capabilities")
        return json.dumps(caps[platform])  # Return as JSON string

config_reader = ConfigReader()

URL = config_reader.get("URL")
REMOTE_URL = config_reader.get("REMOTE_URL")
API_KEY = config_reader.get("API_KEY")
API_HOST = config_reader.get("API_HOST")
API_URL = config_reader.get("API_URL")

PLATFORM = os.getenv("PLATFORM", "windows")
CAPABILITIES = config_reader.get_platform_capabilities(PLATFORM)
TIMESTAMP = os.getenv("TIMESTAMP", "default_time")

print(API_URL)
