import config
import time

def user_login(driver, xpaths):
    conf = config.values()
    driver.get('https://freelancer.com/login')
    driver.set_window_size(800, 600)

    driver.find_element_by_xpath(xpaths['username']).send_keys(conf['username'])
    driver.find_element_by_xpath(xpaths['password']).send_keys(conf['password'])
    driver.find_element_by_xpath(xpaths['login_button']).click()
    time.sleep(25)
    driver.save_screenshot('login.png')
    return driver
