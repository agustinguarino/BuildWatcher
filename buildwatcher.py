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