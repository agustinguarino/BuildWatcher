URL = "https://buildconsole.ulti.io/dashboard/5f1aff213e485000169e317c/builds?page=0&pagesize=20"

LastBuildRow = "//tbody[@role='rowgroup']//tr[4]"
BuildFields = {
    "BuildData": f"{LastBuildRow}//td[1]",
    "DataVersion" : f"{LastBuildRow}//td[2]",
    "BuildUCN" : f"{LastBuildRow}//td[3]",
    "BuildSupersite" : f"{LastBuildRow}//td[4]",
    "BuildFoundation" : f"{LastBuildRow}//td[5]",
    "BuildUES" : f"{LastBuildRow}//td[6]",
    "BuildCommitStatus" : f"{LastBuildRow}//td[7]",
    "BuildPackagingStatus" : f"{LastBuildRow}//td[8]",
    "BuildSmokeStatus" : f"{LastBuildRow}//td[9]",
    "BuildPayrollComplianceStatus" : f"{LastBuildRow}//td[10]",
    "BuildCUHRStatus" : f"{LastBuildRow}//td[11]",
    "BuildIntegDataLaunchStatus" : f"{LastBuildRow}//td[12]",
    "BuildWFNHCMCoreUnifStatus" : f"{LastBuildRow}//td[13]",
    "BuildRwdsTalentTimeStatus" : f"{LastBuildRow}//td[14]",
    "BuildUESStatus" : f"{LastBuildRow}//td[15]",
    "BuildReleaseCandidateStatus" : f"{LastBuildRow}//td[16]",
}

RunTestsButton = "//li[@class='clickable fail ng-star-inserted'][1]//strong"
ViewInTeamCityButton = "//span[text()=' VIEW IN TEAMCITY '][1]"

BuildInformation = {}

Error_Types_List = ["KeyNotFoundException", "IndexOutOfRangeException", "NUnit.Framework.Assert", "InvalidOperationException", "TestFixtureSetUp failed", "ElementNotEnabledException", "SQLException", "NoSuchElementException", "NoSuchRowException", "WebDriverException", "ValuesAreNotEqualException", "NoSuchWindowException", "ElementExistsException", "RecordCountNotEqualException", "NoSuchEnvironmentException"]
Teams_List = ["ObjectModel", "AcceptanceGHR", "MobileAppApi", "Payroll", "TaxCare", "TaxUs", "GlobalBenefits", "UPM", "ImportTool", "GlobalHR"]

Login_Page_Indicator_XPATH = "//a[contains(text(), 'Login with SSO')]"
HomePage_Indicator_XPATH = "(//span[@class='ProjectsTreeItem__name--uT ring-global-ellipsis'])[1]"
Failure_Elements_XPATH = "//div[@class='TestItemAdvanced__nameColumn--eG']"
#Expand_Failure_Arrow_XPATH = "//div[@class='Details__heading--id TestItem__heading--Xx TestItem__expandable--KK']/span[@class='ring-icon-icon SvgIcon__icon--wZ TestItem__arrow--TC']"
Arrow_Down_XPATH = "(//div[@class='Details__heading--id TestItem__heading--Xx TestItem__expandable--KK']/span[@class='ring-icon-icon SvgIcon__icon--wZ TestItem__arrow--TC'])[(iterator)]"
Test_Name_XPATH = "(//a[@data-test-build-test-name-part='name'])[(iterator)]"
#Test_Duration_XPATH = "(//button[@class='ring-button-button ring-dropdown-anchor TestHistoryChart__anchor--wF ring-button-heightS ring-button-text'])[(iterator)]"
Test_Duration_XPATH = "//div[@data-test-build-test-item='duration'][(iterator)]"
Package_Name_XPATH = "(//a[@data-test-build-test-name-part='package'])[(iterator)]"
Secondary_Package_XPATH = "(//div[@class='TestItemAdvanced__nameColumn--eG'])[(iterator)]//span[@class='TestName__suite--fP']"
#Flaky_Test_Indicator_XPATH = "//div[@class='TestItemAdvanced__flakyLabel--Vn']"
Flaky_Test_Indicator_XPATH = "(//div[@class='TestItemAdvanced__nameColumn--eG'])[(iterator)]//span[@class='TestFlakyLabel__label--M5']"
Test_Duration_XPATH = "//div[@class='TestItemAdvanced__durationColumn--n8']//span[@class='ring-button-content']"


#
# BuildConsoleScraper
#

Pipeline_Name_XPATH = "//span[@class='mat-select-min-line ng-tns-c154-2 ng-star-inserted']"
Builds_Table_Row_XPATH = "(//tbody[@role='rowgroup']//tr)[(iterator)]"
Build_Number_XPATH = Builds_Table_Row_XPATH + "//td//a[@style='text-decoration: unset; color: #3f51b5;']"
Build_Date_XPATH = Builds_Table_Row_XPATH + "//td//span[@style='font-size: 12px;']"
Run_Tests_Button_XPATH = "//li[@class='clickable fail ng-star-inserted']"
View_TeamCity_Button_XPATH = "(//a[@class='mat-focus-indicator mat-button mat-button-base'])[2]"
