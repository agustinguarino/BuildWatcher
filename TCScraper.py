from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from time import sleep
import Util as Util
import BuildConsoleScraper as bcs
import sys

urls = bcs.getBuildConsoleUrls(sys.argv[1])
for key in urls.keys():
    print(str(key))

driver = webdriver.Chrome()


headers = "Build #, Build Date, Test Name, Package, Flaky Test, Duration, Stacktrace, Error Category" + "\n"
with open("errors.csv", "a") as file:
            file.write(headers)

for key in urls.keys():
    url = urls[str(key)]
    failure_elements = []

    build_number = str(key).split("/*/")[0]
    build_date = str(key).split("/*/")[1]

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
        error_category = "No error category found."

        try:
            arrow_down = driver.find_element(By.XPATH, Util.Arrow_Down_XPATH.replace("(iterator)", str(i + 1)))
            driver.execute_script("arguments[0].click();", arrow_down)
        except Exception:
            print("Error when trying to click arrow down")

        sleep(0.3)

        # Get test name
        try:
            test_name = driver.find_element(By.XPATH, Util.Test_Name_XPATH.replace("(iterator)", str(i + 1))).text
        except Exception:
            print("Error when trying to get test name.")
        
        # Get package name if present
        try:
            package = driver.find_element(By.XPATH, Util.Package_Name_XPATH.replace("(iterator)", str(i + 1))).text
        except Exception:
            try:
                package = driver.find_element(By.XPATH, Util.Secondary_Package_XPATH.replace("(iterator)", str(i + 1))).text.replace("C:\\Projects\\UltiPro.NET\\distrib\\", "").split(":")[0]
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
            duration = driver.find_element(By.XPATH, Util.Test_Duration_XPATH.replace("(iterator)", str(i + 1))).text
        except Exception:
            duration = "0"

        # Get stacktrace error
        try:
            stacktrace = driver.find_element(By.XPATH, "//div[@data-test-build-log-messages='true']").text[:250]

            for error in Util.Error_Types_List:
                if error.lower() in stacktrace.lower():
                    error_category = error

        except Exception:
            stacktrace = "No stacktrace."

        print(f"{test_name} // {package} // {flaky_test} // {duration} // {stacktrace[:500]}")
        sleep(0.3)

        # Write in csv
        data = f"{build_number}|| {build_date}|| {test_name}|| {package}|| {flaky_test}|| {duration}|| {stacktrace}|| {error_category}".replace(",", ";").replace("||", ",").replace("\n", "") + "\n"

        with open("C:\Projects\BuildWatcher\errors.csv", "a") as file:
            file.write(data)