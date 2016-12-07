from selenium.webdriver.support.wait import WebDriverWait


def login():
    return {
        'username': '//input[@id="username"]',
        'password': '//input[@id="passwd"]',
        'login_button': '//button[@id="login_btn"]'
    }


def search_results(driver):

    # it is just near after what we are looking for:
    WebDriverWait(driver, 15).until(lambda driver: driver.find_element_by_class_name("ProjectTable-description"))
    driver.save_screenshot('screen2.png')
    z = driver.find_elements_by_xpath("//h2[@class='ProjectTable-title']/a")
    return [i.get_attribute('href') for i in z]
