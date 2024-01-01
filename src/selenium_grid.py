import subprocess

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def setup_selenium_grid():
    subprocess.Popen("docker build -t selenium-grid .", shell=True)
    subprocess.Popen("docker run -d -p 4444:4444 --name selenium-grid selenium-grid", shell=True)

def get_webdriver():
    desired_cap = DesiredCapabilities.CHROME
    desired_cap['version'] = 'latest'
    driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', desired_capabilities=desired_cap)
    return driver
