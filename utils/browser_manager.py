from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from robot.api.deco import keyword, library
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
import json
from selenium.common.exceptions import WebDriverException

@library
class BrowserManager:

    @keyword("Launch Browser")
    def launch_browser(self):
        sl = BuiltIn().get_library_instance("SeleniumLibrary")
        sl.open_browser("https://elpais.com", browser="chrome")
        sl.maximize_browser_window()

    @keyword("Open Browser With Caps")
    def open_browser_with_caps(self, remote_url, caps_dict):
        if isinstance(caps_dict, str):
            caps = json.loads(caps_dict)
        else:
            caps = caps_dict

        browser_name = caps.get("browserName", "chrome").lower()
        if browser_name == "chrome":
            options = ChromeOptions()
        elif browser_name == "firefox":
            options = FirefoxOptions()
        elif browser_name == "edge":
            options = EdgeOptions()
        elif browser_name == "safari":
            options = webdriver.SafariOptions()
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")

        for key, value in caps.items():
            options.set_capability(key, value)

        driver = webdriver.Remote(command_executor=remote_url, options=options)
        sl = BuiltIn().get_library_instance("SeleniumLibrary")
        sl.register_driver(driver, alias="RemoteBrowser")

    @keyword(name="Set BrowserStack Status")
    def set_browserstack_status():
        try:
            sl = BuiltIn().get_library_instance("SeleniumLibrary")
            driver = sl.driver
            status = BuiltIn().get_variable_value("${TEST STATUS}", default="failed")
            reason = BuiltIn().get_variable_value("${TEST MESSAGE}", default="Test status unknown")
            executor_object = {
                'action': 'setSessionStatus',
                'arguments': {
                    'status': status,
                    'reason': reason
                }
            }
            command = f'browserstack_executor: {json.dumps(executor_object)}'
            driver.execute_script(command)
            logger.info(f"BrowserStack status updated: {status} - {reason}")
        except Exception as e:
            logger.warn(f"Skipping BrowserStack status update: {e}")

    @keyword("Mark Test Status On BrowserStack")
    def mark_test_status_on_browserstack(self, status: str, reason: str):
        try:
            sl = BuiltIn().get_library_instance("SeleniumLibrary")
            driver = sl.driver
            executor_object = {
                'action': 'setSessionStatus',
                'arguments': {
                    'status': status,
                    'reason': reason
                }
            }
            command = f'browserstack_executor: {json.dumps(executor_object)}'
            driver.execute_script(command)
            logger.info(f"✅ BrowserStack status updated: {status} - {reason}")
        except Exception as e:
            logger.warn(f"❌ Skipping BrowserStack status update: {e}")
