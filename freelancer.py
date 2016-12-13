from selenium import webdriver
import freelancer_xpaths
import freelancer_login
from selenium.webdriver.support.wait import WebDriverWait
import freelancer_projects
import os

# Login
driver = webdriver.PhantomJS()
freelancer_login.user_login(driver, freelancer_xpaths.login())

freelancer_projects.json_open(driver, os.environ['bids_src_url'])
driver.quit()
