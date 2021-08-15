from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv
import time

import requests
from bs4 import BeautifulSoup

# this code scrapes all 34 pages worth of review pages links from the following URL
# the output of this file is links.csv which will be used later to scrape individual reviews

URL = "https://www.tripadvisor.com.sg/Search?q=singapore&searchSessionId=B28AF74AD13390821C8A212BAA7B37061628405941421ssid&searchNearby=false&sid=21509EE97381477CB0B8A840C9F79F5D1628405954198&blockRedirect=true&ssrc=A&rf=8"
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get(URL)

csvFile = open("links.csv", "w", newline='', encoding="utf-8")
csvWriter = csv.writer(csvFile)

time.sleep(2)


# scraping code
for page_num in range(33):
    # sleep required for page to load
    time.sleep(5)

    # extracts a list of attractions each result contains the div of 
    # location , place name and review link of each attraction search result
    results = driver.find_elements_by_xpath("//*[@class='ui_column is-12 content-column result-card']")
    
    # attraction list looped through to extract individual info of 
    # location , place name and review link 
    for result in results:

        # try except used because some of the attraction search results are duds in tripadvisor page and do not contain any of the following tags
        # used to bypass the above error
        try:
            result_obj_link = result.find_element_by_xpath(".//*[@class='review_count']")
            result_link = result_obj_link.get_attribute("href")
            location =  result.find_element_by_xpath(".//*[@class='address-text']").text
            place_name = result.find_element_by_xpath(".//*[@class='result-title']").text
            print(place_name)
            csvWriter.writerow((result_link,location,place_name))  

        except:
            pass
    
    # next button clicked until all 34 pages are done
    pages = driver.find_elements_by_xpath("//*[@class='ui_button nav next primary ']")
    print(pages[0].get_attribute("outerHTML"))
    pages[0].click()

csvFile.close()
driver.close()