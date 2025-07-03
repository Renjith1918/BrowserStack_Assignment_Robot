import json
import os

config_path = os.path.join(os.path.dirname(__file__), 'config.json')
with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

URL = config["URL"]
REMOTE_URL = config["REMOTE_URL"]
platform = os.getenv("PLATFORM", "windows")
CAPABILITIES = config["CAPABILITIES"][platform]