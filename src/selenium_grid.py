import subprocess

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def setup_selenium_grid():
    subprocess.Popen("java -jar selenium-server-standalone.jar -role hub", shell=True)
    subprocess.Popen("java -jar selenium-server-standalone.jar -role node  -hub http://localhost:4444/grid/register", shell=True)

def get_webdriver():
    desired_cap = DesiredCapabilities.CHROME
    desired_cap['version'] = 'latest'
    driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', desired_capabilities=desired_cap)
    return driver
