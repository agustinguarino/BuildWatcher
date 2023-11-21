from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

driver = webdriver.Chrome()

build_id = int(input("Enter build id: "))
runner_name = str(input("Enter runner name: "))
dll_suite_name = str(input("Enter dll suite to search for: "))

pingid_code = str(input("Enter PingID code: "))

url = f"https://teamcity.dev.us.corp/repository/download/UltiPro_V12_4Integration_1Domains_P0QualityGate_00RunTests/{build_id}:id/for_upload_tests.zip!/{runner_name}/{runner_name}/tests/echo/{dll_suite_name}.xml"

def login():
    driver.get("https://teamcity.dev.us.corp/favorite/projects")
    sleep(2)
    driver.find_element(By.XPATH, "//div[@class='buttons']/a").click()
    sleep(2)
    driver.find_element(By.XPATH, "//input[@value='Sign On']").click()
    sleep(2)
    driver.find_element(By.XPATH, "//input[@class='passcode-input']").send_keys(pingid_code)
    sleep(1)
    driver.find_element(By.XPATH, "//input[@class='passcode-input']").send_keys(Keys.ENTER)
    sleep(10)
    WebDriverWait(driver, 120).until(visibility_of_element_located((By.XPATH, "(//span[@class='ProjectsTreeItem__name--uT ring-global-ellipsis'])[1]")))
    driver.get(url)
    sleep(2)

def getDuration():
    duration = driver.find_element(By.XPATH, "(//*[@class='html-attribute-value'])[15]").text
    print(duration)

login()
getDuration()