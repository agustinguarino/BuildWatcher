from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import Util as util

driver = webdriver.Chrome()
driver.get(util.URL)
sleep(10)

for field in util.BuildFields.keys():
    field_data = driver.find_element(By.XPATH, util.BuildFields[field]).text
    util.BuildInformation[field] = field_data
    sleep(1)

print(util.BuildInformation)

for field in util.BuildInformation.keys():
    if "FAILURE" in util.BuildInformation[field]:
        driver.find_element(By.XPATH, f"{util.BuildFields[field]}//div//span").click()
        print("After clicking FAILURE field")
        sleep(5)
        driver.find_element(By.XPATH, util.RunTestsButton).click()
        print("After clicking Run Tests button")
        sleep(1)
        driver.find_element(By.XPATH, util.ViewInTeamCityButton).click()
        print("After clicking View In Teamcity button")
        sleep(20)