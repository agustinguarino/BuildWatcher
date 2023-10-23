from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import Util as util

urls = ["http://teamcity.dev.us.corp/buildConfiguration/UltiPro_V12_4Integration_1Domains_Gate0_00RunTests/52463296?buildTab=tests&status=failed"]
driver = webdriver.Chrome()
FirstRun = True

for url in urls:
    driver.get(url)

    #############################
    if FirstRun:
        FirstRun = False
        print("Sleeping for 30 secs")
        sleep(30)
    #############################

    failure_elements = driver.find_elements(By.XPATH, "")
    