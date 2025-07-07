import os
import json
def get_variables():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(config_path, encoding='utf-8') as f:
        config = json.load(f)

    platform = os.getenv("PLATFORM", "windows")
    timestamp = os.getenv("TIMESTAMP", "default_time")
    capabilities = config["CAPABILITIES"].get(platform)

    if not capabilities:
        raise Exception(f"Invalid platform: {platform}")

    browser = capabilities.get("browserName", "")
    platform_display = f"{platform.capitalize()} - {browser}"

    return {
        "URL": config["URL"],
        "REMOTE_URL": config["REMOTE_URL"],
        "API_KEY": config["API_KEY"],
        "API_HOST": config["API_HOST"],
        "API_URL": config["API_URL"],
        "PLATFORM": platform,
        "PLATFORM_DISPLAY": platform_display,
        "TIMESTAMP": timestamp,
        "CAPABILITIES": json.dumps(capabilities),
    }
