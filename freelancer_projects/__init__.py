import json

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import requests
#from random import randint
import os

def json_open(driver, url):
    r = requests.get(url).text
    data = json.loads(r)
    report=[]
    for i in data['results']:
        report=freelancer_bid(driver, i["bid_details"], i["url"], i['bid_budget'], i["bid_days"], i, report)
    print()
    print('---')
    print()
    print(report)


def freelancer_bid(driver, details, url, budget, days, i, report):
    print()
    print()
    print ('details: ' + details)
    print ('url: ' + url)
    print ('budget: ' + str(budget))
    print ('days: ' + str(days))

    driver.get(url+'#placebid')

    driver.save_screenshot('url.png')

    try:
        WebDriverWait(driver, 210).until(
            lambda driver: driver.find_element_by_xpath("//div[@id='project_status']"))
    except:
            print('Could not find status, skipping')
            try:
                print('Error message is '+driver.find_element_by_xpath("//section[@class='alert alert-block alert-error margin-t20']/h3"))
            except:
                print('Could not find error message')
            leads_update_rest(i)
            return report

    driver.save_screenshot('url.png')
    # skip for project_status != Open
    project_status=driver.find_element_by_xpath("//div[@id='project_status']" ).text
    if(project_status != 'OPEN'):
        print('Skipping, status is '+project_status)
        leads_update_rest(i)
        return report
    if(driver.find_element_by_xpath("//div[@class='user-bid-extension span12']" ).value_of_css_property('display') != 'none'):
        print('Skipping, bid already placed')
        try:
            print(driver.find_element_by_css_selector("div.bid.owner div.bid_description").text)
            send_rest=True
        except:
            print('Error finding current bid description, url saved for report')
            send_rest=False
            report.append('Blank bid: '+url)
        if(send_rest):
            leads_update_rest(i)
        return report

    # budget
    try:
        WebDriverWait(driver, 10).until(
            lambda driver: driver.find_element_by_xpath("//input[@class='margin-b0 margin-l0 input-mini earnedSum']"))
        driver.find_element_by_xpath("//input[@class='margin-b0 margin-l0 input-mini earnedSum']").send_keys(Keys.CONTROL, "a")
        driver.find_element_by_xpath("//input[@class='margin-b0 margin-l0 input-mini earnedSum']").send_keys(str(budget))
    except:
        print('Skipping, possibly an hourly project, saved for report')
        report.append('Hourly project: '+url)
        return report

    # delivery
    WebDriverWait(driver, 10).until(
        lambda driver: driver.find_element_by_xpath("//input[@class='margin-b0 margin-l0 input-mini period']"))
    driver.find_element_by_xpath("//input[@class='margin-b0 margin-l0 input-mini period']").send_keys(Keys.CONTROL, "a")
    driver.find_element_by_xpath("//input[@class='margin-b0 margin-l0 input-mini period']").send_keys(str(days))

    # BID button #2
    try:
        WebDriverWait(driver, 30).until(
            lambda driver: driver.find_element_by_xpath("//a[@id='place-bid']"))
        driver.find_element_by_xpath("//a[@id='place-bid']").click()
    except:
        print("Cannot find bid button #2, skipping, saved screen")
        report.append('No button 2: '+url)
        driver.save_screenshot('bid_button2.png')
        return report

    # spam
    try:
        WebDriverWait(driver, 120).until(
            lambda driver: driver.find_element_by_xpath("//a[@class='LiteModal-cancelAction']"))
        driver.find_element_by_xpath("//a[@class='LiteModal-cancelAction']").click()
    except:
        #on some projects, like recruiter, no modal
        print('Could not close modal')

    # proposal text
    # //textarea[@id='proposalDescription']             # description text area
    # //textarea[@class='span8 margin-0 descr firepath-matching-node']
    driver.save_screenshot('project.png')
    WebDriverWait(driver, 120).until(
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
    leads_update_rest(i)
##########################################################################

def leads_update_rest(i):
    i['bid_submitted']=True
    r = requests.put(os.environ['leads_read_url']+'/bids/'+str(i['id'])+'/',i).text
    print("Sent request to rest "+r)

