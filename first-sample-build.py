from dotenv import load_dotenv
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
# This array 'capabilities' defines the capabilities browser, device and OS combinations where the test will run
load_dotenv()
BUILD_NAME = "browserstack-build-1"
capabilities=[{
      'osVersion': '10',
      'os': 'Windows',
      'browser': 'chrome',
      'browserVersion': 'latest',
      "seleniumVersion": "4.0.0",
      'sessionName': 'Parallel Test 1', # test name
      'buildName': BUILD_NAME # Your tests will be organized within this build
      },
      {
      'osVersion': '10',
      'os': 'Windows',
      'browser': 'firefox',
      'browserVersion': 'latest',
      'seleniumVersion': '4.0.0',
      'sessionName': 'Parallel Test 2',
      'buildName': BUILD_NAME
      },
      {
      'osVersion': 'Big Sur',
      'os': 'OS X',
      'browser': 'safari',
      'browserVersion': 'latest',
      'seleniumVersion': '4.0.0',
      'sessionName': 'Parallel Test 3',
      'buildName': BUILD_NAME
}]
def get_browser_option(browser):
    switcher = {
        "chrome": ChromeOptions(),
        "firefox": FirefoxOptions(),
        "edge": EdgeOptions(),
        "safari": SafariOptions(),
    }
    return switcher.get(browser, ChromeOptions())
#run_session function searches for 'BrowserStack' on duckduckgo.com
def run_session(cap):
  bstack_options = {
      "os" : cap["os"],
      "osVersion" : cap["osVersion"],
      "buildName" : cap["buildName"],
      "sessionName" : cap["sessionName"],
      "seleniumVersion" : cap["seleniumVersion"],
      "userName": '',
      "accessKey": ''
  }
  options = get_browser_option(cap["browser"].lower())
  options.browser_version = cap["browserVersion"]
  options.set_capability('bstack:options', bstack_options)
  driver = webdriver.Remote(
    command_executor='https://hub.browserstack.com/wd/hub',
    options=options)
  driver.get("https://www.duckduckgo.com")
  if not "DuckDuckGo" in driver.title:
      raise Exception("Unable to load duckduckgo page!")
  elem = driver.find_element(By.NAME, "q")
  elem.send_keys("BrowserStack")
  elem.submit()
  try:
      WebDriverWait(driver, 5).until(EC.title_contains("BrowserStack"))
      driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Title matched!"}}')
  except TimeoutException:
      driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": "Title not matched"}}')
  print(driver.title)
  driver.quit()
#The Thread function takes run_session function and each set of capability from the caps array as an argument to run each session parallelly
for cap in capabilities:
  Thread(target=run_session, args=(cap,)).start()