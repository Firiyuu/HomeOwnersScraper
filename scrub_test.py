from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options, DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time
import pandas as pd
import itertools
from pymongo import MongoClient
import datetime
import os

def connect_to_db():
# connect to the collection

    client = MongoClient()

    db = client['facebookmarket']

    col = db['marketplace']

    return col








def find_file():
    path = 'D:\\Sept\\Spectrum\\uploads'
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            if '.csv' in file:
                files.append(os.path.join(r, file))
    return files[0]


def get_links(links):
	df = pd.DataFrame()

	for link in links:
		name = link.get_attribute("innerText")
		url = link.get_attribute("href")
		dict_ = {
			"name": name,
			"url": url,
			}
		print(dict_)
		df.append(dict_)
	return dict_list



driver = webdriver.Firefox(executable_path="D:/Sept/Spectrum/env/geckodriver.exe") #CONFIGURE PATH TO DRIVER
print("Firefox Browser Invoked")
#LOG-IN SESSION
print("I will start scraping!")

url = 'https://ecorp.azcc.gov/PublicBusinessSearch/PublicBusinessInfo?entityNumber=L16030623'
driver.get(url)
time.sleep(15)

## ADDRESS //div[23]/div[2]
## COUNTY //div[23]/div[3]
## AGENT //div[15]/div[2]
## OFFICER INFO //td[1] - TITLE
## OFFICER INFO //td[2] - NAME
## OFFICER INFO //td[4] - ADDRESS

# AUTOMATON
address = driver.find_element_by_xpath("//div[23]/div[2]")
county = driver.find_element_by_xpath("//div[23]/div[3]")
agent = driver.find_element_by_xpath("//div[15]/div[2]")
officer_info = driver.find_elements_by_xpath("//td")

officers = []
for officer in officer_info:
	title = officer.find_element_by_xpath("//td[1]")
	name = officer.find_element_by_xpath("//td[2]")
	address = officer.find_element_by_xpath("//td[4]")
	dict_ = {
	"name": name.get_attribute("innerText"),
	"title": title.get_attribute("innerText"),
	"address": address.get_attribute("innerText")
	}
	officers.append(dict_)


dict_ = {
	"address": name.get_attribute("innerText"),
	"county": county.get_attribute("innerText"),
	"agent": agent.get_attribute("innerText"),
	"officers": officers,
	}


print(dict_)
