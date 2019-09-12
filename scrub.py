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

    db = client['spectrum']

    col = db['scrubbed']

    return col




def scrape_url(url, browser):
	browser.get(url)
	time.sleep(5)

	try:
		title = browser.find_element_by_xpath("//div[@id='marketplace-modal-dialog-title']/span[1]")
		title = title.get_attribute("innerText")
	except NoSuchElementException:
		title = "N/A"


	try:
		location = browser.find_element_by_xpath("//div[@class='fsm fwn fcg']/span[@class='_7yi' and 1]")
		location = location.get_attribute("innerText")
	except NoSuchElementException:
		location = "N/A"
	try:
		price = browser.find_element_by_xpath("//div[@class='_5_md  _2iel']")
		price = price.get_attribute("innerText")
	except NoSuchElementException:
		price = "N/A"


	try:
		condition = browser.find_element_by_xpath("//div[@class='_50f8']")
		condition = condition.get_attribute("innerText")
	except NoSuchElementException:
		condition = "N/A"

	
	try:
		description = browser.find_element_by_xpath("//p/span[1]")
		description = description.get_attribute("innerText")
	except NoSuchElementException:
		description = "N/A"

	try:
		time_ = browser.find_element_by_xpath("//a[@class='_r3j']")
		time_ = time_.get_attribute("title")
	except NoSuchElementException:
		time_ = "N/A"


	if title=='N/A' and location == 'N/A' and price =='N/A' and condition =='N/A':
		pass
	else:

		dict_ = {
		"title": title,
		"location": location,
		"price": price,
		"condition": condition,
		"time": time_,
		"retrieved": str(datetime.datetime.now()),
		"url": url
		}
		print(dict_)
		return dict_

def get_urls(items, browser):
	url_list = []
	for item in items:

		url = item.get_attribute("href")
		url = url.strip()
		if "item"  in str(url):
				
				url_list.append(url)

	return url_list


	
def get_data(url_list, browser):
	df = pd.DataFrame()
	for url in url_list:
		dict_ = scrape_url(url, browser)
		df = df.append(dict_, ignore_index=True)
	print(df.head())
	dictData = df.to_dict(orient='records')
	col = connect_to_db()
	col.insert_many(dictData)



def find_file():
    path = 'D:\\Sept\\Spectrum\\uploads'
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            if '.csv' in file:
                files.append(os.path.join(r, file))
    return files[0]




def get_links(links):
	url_list = []
	df = pd.DataFrame()

	for link in links:
		name = link.get_attribute("innerText")
		url = link.get_attribute("href")
		url_list.append(url)
		dict_ = {
			"name": name,
			"url": url,
			}
		print(dict_)
		df = df.append(dict_, ignore_index=True)
	dictData = df.to_dict(orient='records')
	col = connect_to_db()
	col.insert_many(dictData)
	return url_list


driver = webdriver.Firefox(executable_path="D:/Sept/Spectrum/env/geckodriver.exe") #CONFIGURE PATH TO DRIVER
print("Firefox Browser Invoked")
#LOG-IN SESSION
print("I will start scraping!")

url = 'https://ecorp.azcc.gov/AzAccount?sessionExpired=False'
driver.get(url)
time.sleep(15)

# FILE EXPLORER
file = find_file()
print(file)

df = pd.read_csv(file, encoding = "cp1252")
hoa_series = df['HOA'].tolist()

for hoa in hoa_series:
    print(hoa)

	# AUTOMATON
	business_name_text = driver.find_element_by_xpath("//input[@id='SearchCriteria.quickSearch.BusinessName']")
	business_name_text.click()
	business_name_text.send_keys(hoa)


	business_name_search = driver.find_element_by_xpath("//button/span[@class='glyphicon glyphicon-search' and 1]")
	business_name_search.click()
	time.sleep(2)


	links = driver.find_elements_by_xpath("//td[2]/a[@class='BlueLink' and 1]")

	dict__list = get_links(links)