from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import Util as Util

#urls = ["http://teamcity.dev.us.corp/buildConfiguration/UltiPro_V12_4Integration_1Domains_Gate0_00RunTests/52463296?buildTab=tests&status=failed"]
urls = ["http://teamcity.dev.us.corp/buildConfiguration/UltiPro_V12_4Integration_1Domains_Ues_00RunTests/52453001?buildTab=tests&status=failed"]
driver = webdriver.Chrome()
failure_elements = []

for url in urls:
    print("Sleeping for 45 secs")
    sleep(45)
    driver.get(url)
    print("After sleeping")

    print("Starting scraping")
    sleep(5)
    failure_elements = driver.find_elements(By.XPATH, Util.Failure_Elements_XPATH)
    arrow_elements = driver.find_elements(By.XPATH, Util.Expand_Failure_Arrow_XPATH)
    print(f"Errors detected: {str(len(failure_elements))}")
    print("Ending scraping")


for i in range (0, len(failure_elements)):
    print("Arrive")
    arrow_down = driver.find_element(By.XPATH, f"(//div[@class='Details__heading--id TestItem__heading--Xx TestItem__expandable--KK']/span[@class='ring-icon-icon SvgIcon__icon--wZ TestItem__arrow--TC'])[{str(i + 1)}]")
    driver.execute_script("arguments[0].click();", arrow_down)
    sleep(10)
    test_name = driver.find_element(By.XPATH, f"(//a[@data-test-build-test-name-part='name'])[{str(i + 1)}]").text
    package = driver.find_element(By.XPATH, f"(//a[@data-test-build-test-name-part='package'])[{str(i + 1)}]").text
    stacktrace = driver.find_element(By.XPATH, f"//div[@class='BuildLogMessages__messages--MP']").text
    print(f"{test_name} // {package} // {stacktrace}")
    sleep(0.5)
    