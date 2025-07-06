*** Settings ***
Library    SeleniumLibrary
Library    ../utils/scraper.py
Variables  ../config/config_reader.py
Variables  ../config/robot_variables.py

*** Test Cases ***
Open El Pais On BrowserStack
    [Documentation]    Open El Pais, click Accept if present, scrape & translate articles, close browser
#    Create Webdriver  Remote  command_executor=${REMOTE_URL}  desired_capabilities=${CAPABILITIES}  selenium_options=None
#
#    Maximize Browser Window
#    Sleep    2s
#    ${is_visible}=    Run Keyword And Return Status    Element Should Be Visible    //button[@id='didomi-notice-agree-button']
#    Run Keyword If    ${is_visible}    Click Element    //button[@id='didomi-notice-agree-button']
#    ${articles}    ${repeats}=    Scrape And Translate Articles
#    Log    ${articles}
#    Log    ${repeats}
#    Close Browser
    Set Test Documentation     El Pais Opinion Test on ${PLATFORM_DISPLAY}
    ${soup}=    Navigate To Opinion Section    ${URL}
    ${articles}=    Fetch Top Articles    ${soup}    5
    Print Articles In Spanish    ${articles}
    Download Cover Images    ${articles}    ${PLATFORM}    ${TIMESTAMP}
    ${translated}=    Translate Article Titles    ${articles}
    ${repeated}=    Analyze Repeated Words In Titles    ${translated}
    Log Translation Results    ${translated}    ${repeated}    ${PLATFORM}    ${TIMESTAMP}
#    ${report_path}=    Save Reports Folder    ${platform}
    Set Test Documentation     ✅ Test completed on ${PLATFORM_DISPLAY}

