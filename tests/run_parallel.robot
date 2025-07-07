*** Settings ***
Library           SeleniumLibrary
Library           ../utils/browser_manager.py
Library           ../utils/scraper.py
Variables         ../config/robot_variables.py
Suite Setup       Setup Suite
Suite Teardown    Close Browser

*** Keywords ***
Setup Suite
    Set Suite Documentation    Testing on ${PLATFORM_DISPLAY}
    Launch Browser

Launch Browser
    Log To Console    BrowserStack opening in ${PLATFORM_DISPLAY}...
    Open Browser With Caps    ${REMOTE_URL}    ${CAPABILITIES}
    ${is_mobile}=    Run Keyword And Return Status    Should Contain    ${CAPABILITIES}    deviceName
    IF    not ${is_mobile}
        Maximize Browser Window
    END
    Sleep    5s

Run El Pais Test Steps
    ${soup}=    Navigate To Opinion Section    ${URL}
    ${articles}=    Fetch Top Articles    ${soup}    5
    Print Articles In Spanish    ${articles}
    Download Cover Images    ${articles}    ${PLATFORM}    ${TIMESTAMP}
    ${translated}=    Translate Article Titles    ${articles}
    ${repeated}=    Analyze Repeated Words In Titles   ${translated}
    Log Translation Results    ${translated}    ${repeated}    ${PLATFORM}    ${TIMESTAMP}

Set BrowserStack Status
    ${rc}    ${msg}=    Run Keyword And Ignore Error    Run El Pais Test Steps
    Set Suite Variable    ${TEST STATUS}    ${rc}
    Set Suite Variable    ${TEST MESSAGE}   ${msg}
    ${status}=    Set Variable If    '${rc}' == 'PASS'    passed    failed
    ${reason}=    Set Variable If    '${rc}' == 'PASS'    El Pais test completed successfully    El Pais test failed at some step
    Mark Test Status On BrowserStack    ${status}    ${reason}
    Run Keyword If    '${rc}' != 'PASS'    Fail    ${msg}

*** Test Cases ***
Run El Pais Test on BrowserStack
    [Documentation]    Runs test on remote BrowserStack browser
    [Teardown]    Set BrowserStack Status
    Run El Pais Test Steps
    Set Test Documentation     ✅ Test completed on ${PLATFORM_DISPLAY}
