from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import Util as Util

#options = webdriver.ChromeOptions()
#options.add_argument('--headless')

driver = webdriver.Chrome()

urls = {}

def getBuildConsoleUrls(page_size):
    url = f"https://buildconsole.ulti.io/dashboard/654aa1e7340e6379f892796c/builds?page=0&pagesize={page_size}"
    driver.get(url)
    pipeline = WebDriverWait(driver, 20).until(visibility_of_element_located((By.XPATH, Util.Pipeline_Name_XPATH))).text

    if pipeline == "Quality Development" or pipeline == "UKGPro Core Quality Gate":
        print("P0s Pipeline")
        sleep(10)

        for i in range(0, int(page_size)):
            sleep(0.3)
            build_selector = Util.Builds_Table_Row_XPATH.replace("(iterator)", str(i + 1)) + "//td"

            build_number = driver.find_element(By.XPATH, Util.Build_Number_XPATH.replace("(iterator)", str(i + 1))).text
            build_date = driver.find_element(By.XPATH, Util.Build_Date_XPATH.replace("(iterator)", str(i + 1))).text
            
            try:
                ActionChains(driver).send_keys(Keys.ESCAPE).perform()

                driver.find_element(By.XPATH, build_selector + "[6]").click()
                driver.find_element(By.XPATH, Util.Run_Tests_Button_XPATH).click()

                tc_url = driver.find_element(By.XPATH, Util.View_TeamCity_Button_XPATH).get_attribute("href")

                build_id = tc_url.split("buildId=")[1].split("&buildTypeId=")[0]
                url = f"https://teamcity.dev.us.corp/buildConfiguration/UltiPro_Dev5Quality_4Integration_1Domains_Gate9_00RunTests/{build_id}?buildTab=tests&status=failed"

                urls[build_number + "/*/" + build_date] = url

                ActionChains(driver).send_keys(Keys.ESCAPE).perform()

                try:
                    pass
                except Exception:
                    build_id = "[!]"

            except Exception:
                errors = "[!]"

        return urls
    else:
        print(pipeline)
        print("No pipeline detected.")