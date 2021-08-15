from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv
import time
import os
import sys

# this code extracts out individual reviews based on the attraction links in link.csv file

URL = "https://www.tripadvisor.com.sg/Search?q=singapore&searchSessionId=B28AF74AD13390821C8A212BAA7B37061628405941421ssid&searchNearby=false&sid=21509EE97381477CB0B8A840C9F79F5D1628405954198&blockRedirect=true&ssrc=A&rf=8"
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

time.sleep(2)

dir_path = os.path.dirname(os.path.realpath(__file__))
link_csv_path = dir_path + "/" + "links.csv"

csvFile = open("reviews.csv", "w", newline='', encoding="utf-8")
csvWriter = csv.writer(csvFile)

doneLinkFile = open("link p.csv", "w", newline='', encoding="utf-8")
doneLinkcsvWriter = csv.writer(doneLinkFile)


# below are adjustable variables for the user to change what type of data they want
# 200 review pages are generally used because they are where reviews from 2017 are generally included which is how far back our group wishes to track
# place count is allowed to be set as well as the computer might not be able to handle more than 30 places worth of reviews without crashing due to lack of ram

# --------------------------------------------- ADJUSTER VARIABLES ----------------------------------------------------
# variable to adjust how many places you want 
place_count = 1000
# variable to adjust how many review pages you want to loop through for each page
input_review_loop = 200
# --------------------------------------------- ADJUSTER VARIABLES ----------------------------------------------------

# loop through the csv file
with open(link_csv_path) as file_handler:
    for row in csv.reader(file_handler):
        doneLinkcsvWriter.writerow(row)

        # minus off from adjustable variables
        place_count -= 1

        # pass link to selenium
        url = row[0]
        driver.get(url)

        # output to let user know which link the script is looking
        print()
        print("now looking at: ")
        print(url)
        time.sleep(5)

        # the UI of tripadvisor is an ass there are two type of pages which varies on location
        # thus two type of scrpaing code has to be created and used based on which type of page it is

        # checker variable for what type of page the tripadvisor is displaying
        # if a button from the first page exist, it will contain the selenium obj else it will be empty
        try:
            next_review_first_type = driver.find_element_by_xpath("//a[@class='ui_button nav next primary ']")
        except:
            next_review_first_type = ""

        try:
            next_review_second_type = driver.find_element_by_xpath("//div[@class='_3djM0GaD']/a")
        except:
            next_review_second_type = ""

        # if the first type of button exists it will use the below code (meaning it is displaying the first type of page)
        # scraper code for first type of page
        if next_review_first_type != "":
            pass

            # loop through review pages of attractions
            for j in range(input_review_loop):
                time.sleep(2)
                review = driver.find_elements_by_xpath("//*[@class='Dq9MAugU T870kzTX LnVzGwUB']")
                place_name = driver.find_element_by_tag_name("title")
                place_name_text = place_name.get_attribute("innerHTML").split(" -")[0]
                
                # loop through list of review object on one review page to review individual contents 
                for i in range(len(review)):

                    # try and except used as there are some duds with no data that can cause errors 
                    try:
                        date = review[i].find_element_by_xpath(".//div[@class='_2fxQ4TOx']")
                        date_of_review_text = " ".join(date.text.split()[-2:])
                    except:
                        date_of_review_text = ""
                    
                    try:
                        location = review[i].find_element_by_xpath(".//span[@class='default _3J15flPT small']")
                        location_text = location.text
                    except:
                        location_text = ""

                    try:
                        title = review[i].find_element_by_xpath(".//div[@class='glasR4aX']")
                        title_text = title.text
                    except:
                        location_text = ""

                    try:
                        review_content = review[i].find_element_by_xpath(".//div[@class='cPQsENeY']")
                        review_content_text = review_content.text
                    except:
                        review_content_text

                    try:
                        # date is edited and changed to the same format as the date data in the second page using a dictionary
                        # date has to be changed here as it is not in the date csv data style format originally making it very hard to edit later on
                        date_of_exp = review[i].find_element_by_xpath(".//div[@class='_27JpaCjl']")
                        month_year = date_of_exp.text.split(":")[1]
                        month = month_year.split()[0]
                        year = month_year.split()[1]
                        monthDict= {'January':'Jan', 'February':'Feb', 'March':'Mar', 'April':'Apr', 'May':'May', 'June':'Jun', 'July':'Jul', 'August':'Aug', 'September':'Sep', 'October':'Oct', 'November':'Nov', 'December':'Dec'}
                        edited_month = monthDict[month]
                        date_of_exp_text = edited_month + " " + year
                        
                    except:
                        date_of_exp_text = ""

                    try: 
                        review_num = review[i].find_element_by_xpath(".//div[@class='nf9vGX55']/span")
                        review_num_text = review_num.get_attribute("class").split("_")[-1][0]

                    except:
                        review_num_text = ""
                    
                    # if the review is not empty then it will add it to the csv file
                    if date_of_review_text != "":
                        csvWriter.writerow((place_name_text,date_of_review_text,location_text,title_text,review_content_text,date_of_exp_text,review_num_text))   

                # output to show user which review page it is at
                print("review page", j+1 ,"done")

                # clicker to go to the next page if there is no more next button the loop will move on to the next attraction
                try:
                    next_review_first_type = driver.find_element_by_xpath("//a[@class='ui_button nav next primary ']")
                    next_review_first_type.click()
                except:
                    break

        
        # if the second type of button exists it will use the below code (meaning it is displaying the second type of page)
        # scraper code for second type of page
        else:
            place_name = driver.find_element_by_tag_name("title")
            place_name_text = place_name.get_attribute("innerHTML").split(" -")[0]
            # loop through review pages
            for j in range(input_review_loop):
                time.sleep(5)

                review_list = driver.find_elements_by_xpath("//div[@class='_1c8_1ITO']/div")

                # loop through object to review individual contents 
                for review in review_list:

                    try:
                        date = review.find_element_by_xpath(".//div[@class='DrjyGw-P _26S7gyB4 _1z-B2F-n _1dimhEoy']")
                        date_of_review_text = " ".join(date.text.split()[1:])
                    except:
                        date_of_review_text = ""

                    try:    
                        location = review.find_element_by_xpath(".//div[@class='DrjyGw-P _26S7gyB4 _1dimhEoy']/span")
                        location_text = location.text
                        if location_text.split()[0].isdigit():
                            location_text = ""
                    except:
                        location_text = ""

                    try:
                        title = review.find_element_by_xpath(".//div[@class='DrjyGw-P _1SRa-qNz _19gl_zL- _1z-B2F-n _2AAjjcx8']/span")
                        title_text = title.text
                    except:
                        title_text = ""

                    try:
                        review_num = review.find_element_by_xpath(".//*[name()='svg'][@class='zWXXYhVR']")
                        review_num_text = review_num.get_attribute("aria-label").split()[0]

                    except:                                                
                        review_num_text = ""

                    try:
                        review_content = review.find_element_by_xpath(".//div[@class='cPQsENeY u7nvAeyZ']/div/span")
                        review_content_text = review_content.text
                    except:
                        review_content_text = ""
                        
                    try:
                        date_of_exp = review.find_element_by_xpath(".//div[@class='_3JxPDYSx']")
                        date_of_exp_text = date_of_exp.text.split(" •")[0]
                        

                    except:                                                
                        date_of_exp_text = ""

                    
                    # if the review is not empty
                    if date_of_review_text != "":
                        csvWriter.writerow((place_name_text,date_of_review_text,location_text,title_text,review_content_text,date_of_exp_text,review_num_text))     

                print("review page", j+1 ,"done")

                # click to next page of review if no more next page means end of review
                try:
                    next_review_second_type = driver.find_element_by_xpath("//div[@class='_1I73Kb0a']/div/a")
                except:
                    print("end of all review page")
                    break

                if j != 0:
                    try:
                        next_review_second_type = driver.find_element_by_xpath("//div[@class='_1I73Kb0a']/div/a")
                        next_review_second_type.click()
                    except:
                        break
                else:
                    next_review_second_type.click()
            
        print("place done")

        # if all of the places is finished the entire loop will be stopped
        if place_count == 0:
            break


    print("scraping done")
csvFile.close()
doneLinkFile.close()
driver.close()

# updating the link.csv file to remove what was scraped earlier
updatedLinkFile = open("links_edit.csv", "w", newline='', encoding="utf-8")
updatedLinkWriter = csv.writer(updatedLinkFile)
updatingcount = 0

# open link file and if the row is lesser than the last place count index it will be ignored
# else it will be writeen into links_edit.csv and replace the og link.csv
with open("links.csv") as file_handler:
    for row in csv.reader(file_handler):
        if updatingcount < place_count: 
            pass
        else:
            updatedLinkWriter.writerow(row)
        updatingcount+=1
updatedLinkFile.close()
print("link file updated")
dir_path = os.path.dirname(os.path.realpath(__file__))
link_csv_path = dir_path + "/" + "links.csv"
os.remove(link_csv_path)
os.rename("links_edit.csv","links.csv")
updatedLinkFile.close()