from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import Util as Util

urls = ["https://teamcity.dev.us.corp/buildConfiguration/UltiPro_Dev5Quality_4Integration_1Domains_Gate9_00RunTests/52499069?buildTab=tests&status=failed"]
driver = webdriver.Chrome()
failure_elements = []

for url in urls:
    driver.get(url)

    ## Automate process until get to password and PingID code needed

    print("Sleeping for 45 secs")
    sleep(45)
    driver.get(url)
    print("After sleeping")

    driver.get(url)

    print("Starting scraping")
    sleep(5)
    failure_elements = driver.find_elements(By.XPATH, "//div[@class='TestItem__expandable--KK TestItemAdvanced__row--pF']") # Util.Failure_Elements_XPATH
    print(f"Errors detected: {str(len(failure_elements))}")
    print("Ending scraping")


# For each error element found in TeamCity
for i in range (0, len(failure_elements)):
    print("Arrive")
    arrow_down = driver.find_element(By.XPATH, f"(//div[@class='Details__heading--id TestItem__heading--Xx TestItem__expandable--KK']/span[@class='ring-icon-icon SvgIcon__icon--wZ TestItem__arrow--TC'])[{str(i + 1)}]")
    driver.execute_script("arguments[0].click();", arrow_down)
    sleep(1)

    # Get test name
    test_name = driver.find_element(By.XPATH, f"(//a[@data-test-build-test-name-part='name'])[{str(i + 1)}]").text
    
    # Get package name if present
    try:
        package = driver.find_element(By.XPATH, f"(//a[@data-test-build-test-name-part='package'])[{str(i + 1)}]").text
    except Exception:
        package = "No package found."

    # Get flaky test inficator if present
    try:
        flaky_test_indicator = driver.find_element(By.XPATH, Util.Flaky_Test_Indicator_XPATH).text
        if flaky_test_indicator == "flaky": flaky_test = True
        
    except Exception:
        flaky_test = False

    # Get test duration if present
    try:
        duration = driver.find_element(By.XPATH, Util.Test_Duration_XPATH).text
    except Exception:
        duration = "0"

    # Get stacktrace error
    try:
        stacktrace = driver.find_element(By.XPATH, f"//div[@class='BuildLogMessages__messages--MP']").text
    except Exception:
        stacktrace = "No stacktrace."

    ## Make package optional (some tests dont have the element)
    ## Check for flaky tag
    print(f"{test_name}")
    sleep(0.5)
    