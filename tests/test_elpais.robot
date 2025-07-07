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

*** Test Cases ***
Run El Pais Test Locally
    [Documentation]    Runs test locally on default browser
    ${soup}=    Navigate To Opinion Section    ${URL}
    ${articles}=    Fetch Top Articles    ${soup}    5
    Print Articles In Spanish    ${articles}
    Download Cover Images    ${articles}    Local    ${TIMESTAMP}
    ${translated}=    Translate Article Titles    ${articles}
    ${repeated}=    Analyze Repeated Words In Titles    ${translated}
    Log Translation Results    ${translated}    ${repeated}    Local    ${TIMESTAMP}
    Set Test Documentation     ✅ Test completed on ${PLATFORM_DISPLAY}