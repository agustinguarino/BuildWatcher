from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import datetime
from Util import dlls

build_id = str(input("[!] Enter build id: "))
runner_prefix = str(input("[!] Enter runners prefix: ")).upper()
pingid_code = str(input("[!] Enter PingID code: "))

#dll_suites_list = []
#with open("dlls_list.txt", "r") as file:
#    lines = file.readlines()
#    [dll_suites_list.append(x.replace("\n", "")) for x in lines if x not in dll_suites_list]

folder_variations = ["echo", "nunit3"]

runner_names_list = []
urls = []
results = {}

driver = webdriver.Chrome()

def writeReportHeaders():
    #data = f"Build ID, Runner Name, DLL Suite, Test Duration, XML URL"

    #with open("report.csv", "w") as file:
        #file.write(data + "\n")
        #print("[!] Headers added")

    pass

def generateRunnerNames():
    for i in range(10, 21):
        runner_name = runner_prefix + str(i)
        runner_names_list.append(runner_name)

def parseUrl(runner_name, dll_suite_name):
    if "Echo.Automation." in dll_suite_name:
        folder_name = "echo"
    else:
        folder_name = "nunit3"
        
    url = f"https://teamcity.dev.us.corp/repository/download/UltiPro_V12_4Integration_1Domains_P0QualityGate_00RunTests/{build_id}:id/for_upload_tests.zip!/{runner_name}/{runner_name}/tests/{folder_name}/{dll_suite_name}.xml"
    return url

def generateUrls():
    #for runner_name in runner_names_list:
    #    for dll_suite in dll_suites_list:
    #        for folder in folder_variations:
    #            url = parseUrl(runner_name, dll_suite, folder)
    #            urls.append(url)

    for runner_name in runner_names_list:
        dll_suites = dlls[str(runner_name[-2:])]
        print(f"Suites for runner {runner_name}: {dll_suites}")
        for dll_suite in dll_suites:
            url = parseUrl(runner_name, dll_suite)
            urls.append(url)

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

def startNavigating():
    for i in range(0, len(urls)):
        url = urls[i]
        print(f"[!] Navigating to: {url} ({str(i)}/{str(len(urls))})")
        driver.get(url)

        duration = getDuration(False)

        # Retry with new number of element
        if duration == False:
            duration = getDuration(True)

        if duration is not False:
            print(f"Test duration: {str(duration)}")

            #test_duration = str(datetime.timedelta(seconds= int(duration.split(".")[0])))
            logToReport(url, duration)
        else:
            print("[WARNING] Error getting test suite duration.")

def getDuration(retry):
    try:
        #duration = driver.find_element(By.XPATH, "(//*[@class='html-attribute-value'])[15]").text
        if retry:
            duration = driver.find_element(By.CSS_SELECTOR, "#folder0 > div:nth-child(1) > span.html-tag > span:nth-child(15) > span.html-attribute-value").text
        else:
            duration = driver.find_element(By.CSS_SELECTOR, "#folder0 > div:nth-child(1) > span.html-tag > span:nth-child(16) > span.html-attribute-value").text
    except Exception:
        duration = False
    
    return duration

def logToReport(url, duration):
    splitted_url = str(url).split("/")
    runner_name = splitted_url[8]
    dll_suite = splitted_url[12]

    #data = f"{build_id}, {runner_name}, {dll_suite}, {duration}, {url}"

    #with open("report.csv", "a") as file:
        #file.write(data + "\n")
        #print("[!] Reported")

    try:
        results[runner_name] += float(duration)
        print(f"Saving {float(duration)} in runner {runner_name} for suite {dll_suite}")
    except Exception:
        results[runner_name] = float(duration)
        print(f"Creating {float(duration)} in runner {runner_name} for suite {dll_suite}")

def writeToReport():
    headers = ""
    build_data = ""

    for runner in results.keys():
        headers = f"{headers}{runner},"

        runner_duration = results[runner]
        build_data = f"{build_data}{str(datetime.timedelta(seconds= int(str(runner_duration).split('.')[0])))},"
        #build_data = f"{build_data}{str(int(runner_duration/60))},"

    with open("report.csv", "a") as file:
        file.write("Build Number," + headers + "\n")
        file.write(build_id + "," + build_data + "\n")


# Start logic
writeReportHeaders()
generateRunnerNames()
generateUrls()

for url in urls:
    print(url + "\n")

login()
startNavigating()
writeToReport()