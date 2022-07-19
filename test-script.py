import os
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from threading import Thread
# Other imports and desired_cap definition goes here
desired_cap = {
"os" : "Windows",
"os_version" : "10",
"browser" : "Chrome",
"browser_version" : "latest",
"project" : 'accionSTEMstatistics',
"build" : 'automataSTEM beta',
"name" : 'statistics',
'browserstack.debug': 'true',  # for enabling visual logs
'browserstack.console': 'info',  # to enable console logs at the info level. You can also use other log levels here
'browserstack.networkLogs': 'true'  # to enable network logs to be logged
}


username = os.environ['BROWSERSTACK_USERNAME'];
accessKey = os.environ['BROWSERSTACK_ACCESS_KEY'];
driver = webdriver.Remote(
    command_executor='https://'+username+':'+accessKey+'@hub-cloud.browserstack.com/wd/hub',
    desired_capabilities=desired_cap
    )


# get web
driver.get('https://www.khanacademy.org/teacher/class/SNFD6RAV/overview/activity')
driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Yaay! my sample test passed"}}')
driver.quit()
# Rest of the test case goes here