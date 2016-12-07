from selenium import webdriver
import freelancer_xpaths
import freelancer_login
from selenium.webdriver.support.wait import WebDriverWait


# Login
driver = webdriver.PhantomJS()
freelancer_login.user_login(driver, freelancer_xpaths.login())

driver.quit()
