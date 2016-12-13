import json

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import requests

def json_open(driver, url):
    r = requests.get(url).text
    data = json.loads(r)
    for i in data['results']:
        freelancer_bid(driver, i["bid_details"], i["url"], i['bid_budget'], i["bid_days"])


def freelancer_bid(driver, details, url, budget, days):
    print ('my driver: ' + str(driver))
    print ('details: ' + details)
    print ('url: ' + url)
    print ('budget: ' + str(budget))
    print ('days: ' + str(days))

    # load jobs url
    WebDriverWait(driver, 60).until(lambda driver: driver.find_element_by_xpath("//h3[@class='dashboard-section-heading']"))
    print(url)
    driver.get(url)

    try:
        ##################### darn chat is in the way ####################
        WebDriverWait(driver, 30).until(
            lambda driver: driver.find_element_by_xpath("//button[@class='ContactList-action-button']"))
        driver.find_element_by_xpath("//button[@class='ContactList-action-button']").click()

        WebDriverWait(driver, 30).until(
            lambda driver: driver.find_element_by_xpath("//button[@ng-click='ContactListSettings.minimise($event)']"))
        driver.find_element_by_xpath("//button[@ng-click='ContactListSettings.minimise($event)']").click()
        ##################### /darn chat is in the way ##################
    except:
        print("Failed to minimize chat")

    # BD button #1
    WebDriverWait(driver, 30).until(lambda driver: driver.find_element_by_xpath("//a[@class='btn btn-info btn-large bidButton']"))
    driver.find_element_by_xpath("//a[@class='btn btn-info btn-large bidButton']").click()

    # budget
    WebDriverWait(driver, 30).until(
        lambda driver: driver.find_element_by_xpath("//input[@class='margin-b0 margin-l0 input-mini earnedSum']"))
    driver.find_element_by_xpath("//input[@class='margin-b0 margin-l0 input-mini earnedSum']").send_keys(Keys.CONTROL, "a")
    driver.find_element_by_xpath("//input[@class='margin-b0 margin-l0 input-mini earnedSum']").send_keys(str(budget))

    # delivery
    WebDriverWait(driver, 30).until(
        lambda driver: driver.find_element_by_xpath("//input[@class='margin-b0 margin-l0 input-mini period']"))
    driver.find_element_by_xpath("//input[@class='margin-b0 margin-l0 input-mini period']").send_keys(Keys.CONTROL, "a")
    driver.find_element_by_xpath("//input[@class='margin-b0 margin-l0 input-mini period']").send_keys(str(days))

    # BID button #2
    WebDriverWait(driver, 30).until(
        lambda driver: driver.find_element_by_xpath("//a[@class='btn btn-info btn-large ']"))
    driver.find_element_by_xpath("//a[@class='btn btn-info btn-large ']").click()

    # spam
    WebDriverWait(driver, 30).until(
        lambda driver: driver.find_element_by_xpath("//a[@class='LiteModal-cancelAction']"))
    driver.find_element_by_xpath("//a[@class='LiteModal-cancelAction']").click()

    # proposal text
    # //textarea[@id='proposalDescription']             # description text area
    # //textarea[@class='span8 margin-0 descr firepath-matching-node']
    driver.save_screenshot('project.png')
    WebDriverWait(driver, 30).until(
        lambda driver: driver.find_element_by_xpath("//textarea[@id='proposalDescription']"))
    driver.save_screenshot('project2.png')
    driver.find_element_by_xpath("//textarea[@id='proposalDescription']").click()
    driver.find_element_by_xpath("//textarea[@id='proposalDescription']").send_keys(details)

    # optionally - Description of the milestone
    # # //input[@id='milestone-descr-1']                  # milestone description
    # # //input[@class='milestone-proposal-input']
    # WebDriverWait(driver, 30).until(
    #         lambda driver: driver.find_element_by_xpath("//input[@id='milestone-descr-1']"))
    # driver.find_element_by_xpath("//input[@id='milestone-descr-1']").click()
    #
    # # //input[@id='milestone-amount-1']                 # milestone amount
    # # //input[@class='span2']
    # WebDriverWait(driver, 30).until(
    #         lambda driver: driver.find_element_by_xpath("//input[@id='milestone-amount-1']"))
    # driver.find_element_by_xpath("//input[@id='milestone-amount-1']").click()
    # //span[@class='milestone-link-text']  # add another milestone

    # submit proposal
    # //button[@id='place-bid-step2']               # submit button
    # //button[@class='btn btn-info btn-small']
    #WebDriverWait(driver, 30).until(lambda driver: driver.find_element_by_xpath("//button[@id='place-bid-step2']"))
    driver.find_element_by_xpath("//button[@id='place-bid-step2']").click()
    # WebDriverWait(driver, 30).until(lambda driver: driver.find_element_by_xpath("//a[@class='btn btn-large btn-primary align-c margin-t10 repostProjectButton']"))

##########################################################################
