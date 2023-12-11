from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from time import sleep
from Util import *
from BuildConsoleScraper import *
import sys

urls = getBuildConsoleUrls(30)
for key in urls.keys():
    print(str(key))

driver = webdriver.Chrome()
file_name = "Weekly Report 4th-8th"

rca_category = ""
failure_percentage_template = "https://kibana.trove.ukg.int/app/visualize?security_tenant=global#/edit/ad4157c0-92e9-11ee-9ad4-b9a773c5ae9d?_g=(filters:!(),refreshInterval:(pause:!t,value:0),time:(from:now-1y,to:now))&_a=(filters:!((%27$state%27:(store:appState),meta:(alias:!n,disabled:!f,index:%27610f8d00-37ff-11ec-b243-453e049a0a17%27,key:product.keyword,negate:!f,params:(query:ukgpro),type:phrase),query:(match_phrase:(product.keyword:ukgpro))),(%27$state%27:(store:appState),meta:(alias:!n,disabled:!f,index:%27610f8d00-37ff-11ec-b243-453e049a0a17%27,key:gate.keyword,negate:!f,params:(query:P0),type:phrase),query:(match_phrase:(gate.keyword:P0)))),linked:!f,query:(language:kuery,query:WithholdingFormValidationUSA),uiState:(vis:(params:(sort:(columnIndex:3,direction:asc)))),vis:(aggs:!((enabled:!t,id:%273%27,params:(customLabel:%27%27),schema:metric,type:count),(enabled:!t,id:%275%27,params:(field:fullName.keyword,missingBucket:!f,missingBucketLabel:Missing,order:desc,orderBy:_key,otherBucket:!f,otherBucketLabel:Other,size:50000),schema:bucket,type:terms),(enabled:!t,id:%274%27,params:(field:status.keyword,missingBucket:!f,missingBucketLabel:Missing,order:desc,orderBy:%273%27,otherBucket:!f,otherBucketLabel:Other,size:3),schema:splitcols,type:terms)),params:(addRowNumberColumn:!f,computedColsPerSplitCol:!f,computedColumns:!((alignment:left,applyAlignmentOnTitle:!t,applyAlignmentOnTotal:!t,applyTemplate:!f,applyTemplateOnTotal:!t,cellComputedCss:%27%27,computeTotalUsingFormula:!f,customColumnPosition:%27%27,datePattern:%27MMMM%20Do%20YYYY,%20HH:mm:ss.SSS%27,enabled:!t,format:number,formula:%27col1%20%2F%20(col1%20%2B%20col2)%20*%20100%27,label:%27Pass%20Rate%27,pattern:%270,0.%5B00%5D%27,template:%7B%7Bvalue%7D%7D)),csvEncoding:utf-8,csvExportWithTotal:!f,filterAsYouType:!f,filterBarHideable:!f,filterBarWidth:%2725%25%27,filterCaseSensitive:!f,filterHighlightResults:!f,filterTermsSeparately:!f,hideExportLinks:!f,linesComputedFilter:%27col3%20%3C%20100%27,perPage:20,showFilterBar:!f,showMetricsAtAllLevels:!f,showPartialRows:!f,showTotal:!f,sort:(columnIndex:!n,direction:!n),stripedRows:!f,totalFunc:sum),title:%27Test%20Failure%20%25%27,type:enhanced-table))"
failure_percentage_link = ""

headers = "Build #, Build Date, Test Name, Package, Team, Flaky Test, Duration, Stacktrace, Error Category, RCA Category, Failure %" + "\n"
with open(f"C:\Projects\BuildWatcher\{file_name}.csv", "a") as file:
            file.write(headers)

print("Starting")
for key in urls.keys():
    print("Inside")
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
        package_team = "No team found for this package."

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

        # Get filure % link
        failure_percentage_link = failure_percentage_template.replace("WithholdingFormValidationUSA", str(test_name))
        
        # Get package name if present
        try:
            package = driver.find_element(By.XPATH, Util.Package_Name_XPATH.replace("(iterator)", str(i + 1))).text
        except Exception:
            try:
                package = driver.find_element(By.XPATH, Util.Secondary_Package_XPATH.replace("(iterator)", str(i + 1))).text.replace("C:\\Projects\\UltiPro.NET\\distrib\\", "").split(":")[0]
            except Exception:
                package = "No package found."

        # Get team name from package
        for team in Util.Teams_List:
            if team in package:
                package_team = team

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
            stacktrace = driver.find_element(By.XPATH, "//div[@data-test-build-log-messages='true']").text[:800]

            for error in Util.Error_Types_List:
                if error.lower() in stacktrace.lower():
                    error_category = error

        except Exception:
            stacktrace = "No stacktrace."

        # Get RCA Category
        if "the connection is broken and recovery is not possible" in str(stacktrace).lower() or "cannot open database" in str(stacktrace).lower():
            rca_category = "Database Connection"
        elif "Cannot insert duplicate key in object".lower() in str(stacktrace).lower():
            rca_category = "Database"
        else:
            rca_category = "Test" 

        print(f"{test_name} // {package} // {flaky_test} // {duration} // {stacktrace[:750]}")
        sleep(0.3)

        # Write in csv
        data = f"{build_number}|| {build_date}|| {test_name}|| {package}|| {package_team}|| {flaky_test}|| {duration}|| {stacktrace}|| {error_category}|| {rca_category}|| {failure_percentage_link}".replace(",", ";").replace("||", ",").replace("\n", "") + "\n"

        with open(f"C:\Projects\BuildWatcher\{file_name}.csv", "a") as file:
            file.write(data)