*** Settings ***
Library    AppiumLibrary
Library    BrowserstackLibrary  username=robotcourses_P7GMVF  access_key=yAs2TMrqtBUnAfS8EHqX
Test Teardown    Run Keywords
...    Update Test Case Status in BrowserStack
...    Close Application
Resource    base.resource

*** Test Cases ***
Olá Mundo
    ${bs_url}  Upload Application to Browserstack
    ...    app_name=ted.apk
    ...    app_path=app/app.apk
    ...    custom_id=TED_OUVINTE_123

    Open Application
    ...  remote_url=http://robotcourses_P7GMVF:yAs2TMrqtBUnAfS8EHqX@hub.browserstack.com:80/wd/hub
    ...  automationName=uiautomator2
    ...  platformName=${PLATFORM_NAME}
    ...  deviceName=${DEVICE_NAME}
    ...  app=${bs_url}
    ...  project=${BROWSERSTACK_PROJECT}
    ...  build=TED
    ...  name=${TEST_NAME}
    ...  bstack:options=${BROWSERSTACK_OPTIONS}
    ...  browserstack.networkLogs=${True}
    ...  browserstack.networkLogsOptions.captureContent=${True}
    ...  autoGrantPermissions=${True}
    ...  autoAcceptAlerts=${True}
    ...  disableIdLocatorAutocompletion=${True}
    ...  browserstack.idleTimeout=60
    ...  interactiveDebugging=${True}
    
    Wait Until Element Is Visible    Next
    Click Element    Nexts