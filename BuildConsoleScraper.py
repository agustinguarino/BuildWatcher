from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import Util as Util

driver = webdriver.Chrome()

urls = {}

def getBuildConsoleUrls():
    url = "https://buildconsole.ulti.io/dashboard/64e62b8a1aa339d31db3edf1/builds?page=0&pagesize=20"
    driver.get(url)
    pipeline = WebDriverWait(driver, 20).until(visibility_of_element_located((By.XPATH, Util.Pipeline_Name_XPATH))).text

    if pipeline == "Quality Development":
        print("P0s Pipeline")
        sleep(10)

        for i in range(1, 20):
            sleep(0.3)
            build_selector = Util.Builds_Table_Row_XPATH.replace("(iterator)", str(i)) + "//td"

            build_number = driver.find_element(By.XPATH, Util.Build_Number_XPATH.replace("(iterator)", str(i + 1))).text
            build_date = driver.find_element(By.XPATH, Util.Build_Date_XPATH.replace("(iterator)", str(i + 1))).text
            
            try:
                ActionChains(driver).send_keys(Keys.ESCAPE).perform()

                driver.find_element(By.XPATH, build_selector + "//span[@ng-reflect-ng-class='failure-text']").click()
                driver.find_element(By.XPATH, Util.Run_Tests_Button_XPATH).click()

                tc_url = driver.find_element(By.XPATH, Util.View_TeamCity_Button_XPATH).get_attribute("href")

                ActionChains(driver).send_keys(Keys.ESCAPE).perform()

                try:
                    build_id = tc_url.split("buildId=")[1].split("&buildTypeId=")[0]
                    url = f"https://teamcity.dev.us.corp/buildConfiguration/UltiPro_Dev5Quality_4Integration_1Domains_Gate9_00RunTests/{build_id}?buildTab=tests&status=failed"
                    
                    urls[build_number + "/*/" + build_date] = url
                except Exception:
                    build_id = "[!]"

            except Exception:
                errors = "[!]"

        return urls