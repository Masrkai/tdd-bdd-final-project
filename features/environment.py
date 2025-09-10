"""
Environment for Behave Testing
"""
from os import getenv
from selenium import webdriver

WAIT_SECONDS = int(getenv('WAIT_SECONDS', '30'))
BASE_URL = getenv('BASE_URL', 'http://localhost:5000')
DRIVER = getenv('DRIVER', 'chrome').lower()  # Changed default to chrome
BRAVE_PATH = getenv('BRAVE_PATH', '/run/current-system/sw/bin/brave')  # Path to Brave executable


def before_all(context):
    """ Executed once before all tests """
    context.base_url = BASE_URL
    context.wait_seconds = WAIT_SECONDS
    # Select either Chrome/Brave or Firefox
    if 'firefox' in DRIVER:
        context.driver = get_firefox()
    else:
        context.driver = get_chrome()
    context.driver.implicitly_wait(context.wait_seconds)
    context.config.setup_logging()


def after_all(context):
    """ Executed after all tests """
    context.driver.quit()

######################################################################
# Utility functions to create web drivers
######################################################################

def get_chrome():
    """Creates a headless Chrome driver (can use Brave browser)"""
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")  # Added for stability
    options.add_argument("--disable-gpu")  # Added for headless stability
    
    # If Brave path is specified, use Brave browser
    if BRAVE_PATH:
        options.binary_location = BRAVE_PATH
    
    return webdriver.Chrome(options=options)


def get_firefox():
    """Creates a headless Firefox driver"""
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    return webdriver.Firefox(options=options)