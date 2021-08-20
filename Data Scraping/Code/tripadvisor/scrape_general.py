from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv
import time

# create CSV file
csvFile = open("reviews.csv", "w", newline='', encoding="utf-8")
csvWriter = csv.writer(csvFile)
csvWriter.writerow(['places','review',"review_num"])

URL = "https://www.tripadvisor.com.sg/Search?q=singapore&searchSessionId=B28AF74AD13390821C8A212BAA7B37061628405941421ssid&searchNearby=false&sid=21509EE97381477CB0B8A840C9F79F5D1628405954198&blockRedirect=true&ssrc=A&rf=9"

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get(URL)

# sleep to let the thing run and bypass their blocks
time.sleep(5)

for page_num in range(1,32):

    time.sleep(10)

    if page_num != 1:
        pages = driver.find_elements_by_xpath("//*[@class='ui_button nav next primary ']")
        print(pages[0].get_attribute("outerHTML"))
        pages[0].click()
        time.sleep(5)

    # take out cards of data in this case it would return a list as an output
    results = driver.find_elements_by_xpath("//*[@class='ui_column is-12 content-column result-card']")
    # print(results[0].get_attribute("innerHTML"))

    for i in range(len(results)):
        # returns place inside the element of the list output is a list
        place = results[i].find_elements_by_xpath(".//div[@class='result-title']")
        # may or may not have data so an if/else condition is used to fill in null data
        if len(place) > 0: 
            place_name = place[0].text
        else:
            place_name = ''

        # review number
        review_num = results[i].find_elements_by_xpath(".//div[@class='prw_rup prw_common_responsive_rating_and_review_count']")
        if len(review_num) > 0:
            review_number = review_num[0].text
        else:
            review_number = ''
    
        # review rating
        rating = results[i].find_elements_by_xpath(".//*[@class='prw_rup prw_common_responsive_rating_and_review_count']/span")
        if len(rating) > 0:
            rating_number = rating[0].get_attribute("alt").split()[0]
        else:
            rating_number = ''     
        
        # put data as row in a csv file
        if place_name != "":
            csvWriter.writerow((place_name,review_number,rating_number))   


csvFile.close()
driver.close()