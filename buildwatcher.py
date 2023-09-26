from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import Util as util

driver = webdriver.Chrome()
driver.get(util.URL)
sleep(10)

build_number = driver.find_element(By.XPATH, util.BuildData).text
print(build_number)