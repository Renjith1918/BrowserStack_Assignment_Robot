*** Settings ***
Library    SeleniumLibrary
Library    ../utils/scraper.py
Variables  ../config/robot_variables.py

*** Test Cases ***
Open El Pais On BrowserStack
    [Documentation]    Open El Pais, click Accept if present, scrape & translate articles, close browser
    Open Browser    ${URL}    remote_url=${REMOTE_URL}    desired_capabilities=${CAPABILITIES}
    Maximize Browser Window
    Sleep    2s
    ${is_visible}=    Run Keyword And Return Status    Element Should Be Visible    //button[@id='didomi-notice-agree-button']
    Run Keyword If    ${is_visible}    Click Element    //button[@id='didomi-notice-agree-button']
    ${articles}    ${repeats}=    Scrape And Translate Articles
    Log    ${articles}
    Log    ${repeats}
    Close Browser
