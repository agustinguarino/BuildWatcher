from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import Util as Util

urls = ["http://teamcity.dev.us.corp/buildConfiguration/UltiPro_V12_4Integration_1Domains_Gate0_00RunTests/52463296?buildTab=tests&status=failed"]
driver = webdriver.Chrome()
FirstRun = True
failure_elements = []
failure_links = []

for url in urls:
    driver.get(url)

    #############################
    if FirstRun:
        FirstRun = False
        print("Sleeping for 50 secs")
        sleep(50)
        driver.get(url)
        print("After sleeping")
    #############################

    print("Starting scraping")
    sleep(5)
    failure_elements = driver.find_elements(By.XPATH, Util.Failure_Elements_XPATH)
    print(f"Errors detected: {str(len(failure_elements))}")
    print("Ending scraping")

print("Starting printing")
total = 0
for i in range(0, len(failure_elements)):
    if i % 4 == 0:
        failure_links.append(failure_elements[i].get_attribute("href"))
        print("URL: " , failure_elements[i].get_attribute("href"))
        total += 1

print(f"Ending printing ({str(total)})")
    