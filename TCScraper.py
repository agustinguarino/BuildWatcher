from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from time import sleep
import Util as Util
import xlsxwriter as xlsx
import os

urls = ["https://teamcity.dev.us.corp/buildConfiguration/UltiPro_Dev5Quality_4Integration_1Domains_Gate9_00RunTests/52530534?buildTab=tests&status=failed"]
#urls = ["https://teamcity.dev.us.corp/buildConfiguration/UltiPro_Dev5Quality_4Integration_1Domains_Gate9_00RunTests/52739671?buildTab=tests&status=failed"]
driver = webdriver.Chrome()
failure_elements = []
column = 0
row = 0

for url in urls:
    driver.get("https://teamcity.dev.us.corp/favorite/projects")

    ## Automate process until get to password and PingID code needed

    try:
        login_locator = driver.find_element(By.XPATH, Util.Login_Page_Indicator_XPATH)
        login_locator.click()
        WebDriverWait(driver, 120).until(visibility_of_element_located((By.XPATH, Util.HomePage_Indicator_XPATH)))
    except Exception:
        pass

    driver.get(url)

    sleep(5)
    failure_elements = driver.find_elements(By.XPATH, "//div[@class='TestItem__expandable--KK TestItemAdvanced__row--pF']") # Util.Failure_Elements_XPATH
    print(f"Errors detected: {str(len(failure_elements))}")


# For each error element found in TeamCity
for i in range (0, len(failure_elements)):
    print("Arrive")
    arrow_down = driver.find_element(By.XPATH, Util.Arrow_Down_XPATH.replace("(iterator)", str(i + 1)))
    driver.execute_script("arguments[0].click();", arrow_down)
    sleep(0.3)

    # Get test name
    test_name = driver.find_element(By.XPATH, Util.Test_Name_XPATH.replace("(iterator)", str(i + 1))).text.replace(",", ";")
    
    # Get package name if present
    try:
        package = driver.find_element(By.XPATH, Util.Package_Name_XPATH.replace("(iterator)", str(i + 1))).text.replace(",", ";")
    except Exception:
        try:
            package = driver.find_element(By.XPATH, Util.Secondary_Package_XPATH.replace("(iterator)", str(i + 1))).text.split(":")[0].replace(",", ";")
        except Exception:
            package = "No package found."

    # Get flaky test inficator if present
    try:
        flaky_test_indicator = driver.find_element(By.XPATH, Util.Flaky_Test_Indicator_XPATH.replace("(iterator)", str(i + 1))).text
        if flaky_test_indicator == "flaky": flaky_test = "True"
        
    except Exception:
        flaky_test = "False"

    # Get test duration if present
    try:
        duration = driver.find_element(By.XPATH, Util.Test_Duration_XPATH).text.replace(",", ";")
    except Exception:
        duration = "0"

    # Get stacktrace error
    try:
        #stacktrace = driver.find_element(By.XPATH, f"//div[@class='BuildLogMessages__messages--MP']").text[:250].replace("\n", "")
        stacktrace = driver.find_element(By.XPATH, "//div[@data-test-build-log-messages='true']").text[:250].replace(",", ";")
    except Exception:
        stacktrace = "No stacktrace."

    ## Make package optional (some tests dont have the element)
    ## Check for flaky tag
    print(f"{test_name} // {package} // {flaky_test} // {duration} // {stacktrace[:200]}")
    sleep(0.3)

    # Write in csv
    #wb = xlsx.Workbook('data.xlsx')
    #ws = wb.add_worksheet()

    #data = [test_name, package, flaky_test, duration, stacktrace[:200]]
    data = f"{test_name}, {package}, {flaky_test}, {duration}, {stacktrace}"
    #ws.write_row(row, column, tuple(data))
    #row += 1

    with open("errors.csv", "a") as file:
        file.write(data.replace("\n", "") + "\n")