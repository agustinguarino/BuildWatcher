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

Failure_Elements_XPATH = "//div[@class='TestItem__expandable--KK TestItemAdvanced__row--pF']/div[@class='TestItemAdvanced__nameColumn--eG']/span/div/div/a"