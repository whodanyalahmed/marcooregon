import time
from bs4 import BeautifulSoup
from selenium import webdriver
from bs4.element import Tag
from parsel import Selector
# import parameters
import random
import os
import pandas as pd
from selenium.webdriver.support.ui import Select
# import by from selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
# import Expected Condition from selenium
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# os.popen('chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\\Users\\Daniyal\\AppData\\Local\\Google\\Chrome\\User Data" --profile-directory="Default"')


def chrome(headless=False):
    # support to get response status and headers
    d = webdriver.DesiredCapabilities.CHROME
    d['loggingPrefs'] = {'performance': 'ALL'}
    opt = webdriver.ChromeOptions()
    if headless:
        opt.add_argument("--headless")
    opt.add_experimental_option('excludeSwitches', ['enable-logging'])
    opt.add_argument("--disable-popup-blocking")
    # use chrome default profile
    # opt.add_argument('--remote-debugging-port=9222')
    # opt.add_argument(
    # '--user-data-dir=C:\\Users\\Daniyal\\AppData\\Local\\Google\\Chrome\\User Data')
    # opt.add_argument('--profile-directory=Default')
    browser = webdriver.Chrome(
        executable_path=r'i://clients//chromedriver.exe', options=opt, desired_capabilities=d)
    browser.implicitly_wait(10)
    browser.maximize_window()
    return browser


# Pass True if you want to hide chrome browser
driver = chrome(True)
# go to web https://www.modular11.com/schedule?year=21
try:
    driver.get("https://system.gotsport.com/org_event/events/5802")
    time.sleep(5)
    print("Successfully opened the browser and navigated to the website")
except Exception as e:
    print("error : ", e)

try:
    source = driver.page_source
    soup = BeautifulSoup(source, 'lxml')
    # print(soup.prettify())
    # find element by id 'boys'
    boys = soup.find('div', {'id': 'boys'})
    # print(boys)

    # find anchor tag which has a 'group' keyword in href

    groups = boys.find_all('a')
    url = "https://system.gotsport.com"

    def get_group_links(groups):
        boys_leagues = []
        for group in groups:
            # get group attribute href
            link = group.get('href')
            if("schedules?group" in link):
                boys_leagues.append(url+link)
                print(link)
        return boys_leagues
    boys_leagues = get_group_links(groups) 
    try:
        # get the link with URL+'#girls' and click
        girls = driver.find_element_by_xpath('//a[@href="#girls"]')
        girls.click()
        # time.sleep(2)
        
        girls = soup.find('div', {'id': 'girls'})
        # print(girls)

        # find anchor tag which has a 'group' keyword in href

        girls_groups = girls.find_all('a')
        girls_league = get_group_links(girls_groups)
    except Exception as e:
        print(e)
         
except Exception as e:
    print(e)


def get_max_match(leagues):
    li = []
    for league in leagues:
        try:
            driver.get(league)
            # move to end of the page
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            # get source code
            source = driver.page_source
            soup = BeautifulSoup(source, 'lxml')
            # print(soup.prettify())
            # find the last table tag
            table = soup.find_all(
                'table', {'class': 'table table-bordered table-condensed table-hover'})
            # print(table[-1])
            # get tr tag from tbody
            tbody = table[-1].find_all('tbody')

            trs = tbody[0].find_all('tr')
            max_values = []
            for tr in trs:
                td = tr.find('td')
                # remove new line character
                # td = td.replace('\n', '')
                # print(td)
                
                if(td is not None):
                    # print(td.text)
                    # td = td.text.strip('\n')
                    max_values.append(td.text)
                    
            val = str(max(max_values)).replace('\n', '')
            print("The count for this url is: " + val)
            li.append(val)
            # print("successfully loaded the page")

        except Exception as e:
            print(e)
    return li


boys = get_max_match(boys_leagues)
girls = get_max_match(girls_league)
print("boys: " + str(boys))
print('girls: ' ,str(girls))
