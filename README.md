# El País Opinion Scraper & Translator (Robot Framework)

This Robot Framework automation project performs end-to-end scraping, translation, and analysis of articles from the *Opinion* section of [https://elpais.com/], a leading Spanish news outlet.

---

## 📌 Features

✔️ Scrapes top 5 opinion articles from El País  
✔️ Extracts titles, content, and saves cover images (if present)  
✔️ Translates article titles and content from Spanish to English using [Google Translate API on RapidAPI](https://rapidapi.com/googlecloud/api/google-translate1/)  
✔️ Analyzes repeated meaningful words in translated headers  
✔️ Configured for local execution & **parallel test execution** on [BrowserStack](https://www.browserstack.com/)

---
## ✅ Features

- 🌐 Opens El País Opinion section remotely on BrowserStack
- 👁️ Handles cookie consent popup if it appears
- 🧾 Scrapes titles and content of top 5 opinion articles
- 🌍 Translates Spanish content into English using Google Translate API
- 🖼️ Downloads article images (if available)
- 📊 Analyzes translated content for frequently repeated meaningful words
- 🧾 Generates a comprehensive log file `translation_log.txt`

---

## 🚀 Setup Instructions

### 1. 📦 Install Dependencies

Ensure Python 3.7+ is installed, then install all required packages:

pip install -r requirements.txt

### 2. Configure Credentials

Edit the file config/config.json:

{
  "URL": "https://elpais.com/opinion/",
  "API_KEY": "<your_rapidapi_key>",
  "API_HOST": "google-translate113.p.rapidapi.com",
  "API_URL": "https://google-translate113.p.rapidapi.com/api/v1/translator/text",
  "REMOTE_URL": "https://<username>:<access_key>@hub-cloud.browserstack.com/wd/hub",
  "CAPABILITIES": {
    "browserName": "Chrome",
    "browserVersion": "latest",
    "bstack:options": {
      "os": "Windows",
      "osVersion": "10",
      "buildName": "ElPais Suite",
      "sessionName": "ElPais Test",
      "seleniumVersion": "4.14.0"
    }
  }
}

### 3. How to Run the Test

open terminal at root folder and run below command

**robot --outputdir results .\tests\test_elpais.robot**

**Test will:**
  1. Launch browser on BrowserStack  
  2. Visit the Opinion section of El País  
  3. Handle cookie popup (if any)  
  4. Scrape, translate, and save article data

### 4. Output Files
1.translation_log.txt – Contains:
    a. Translated titles and contents
    b. Word frequency summary
    c. API status
2. images/article_0.jpg to article_4.jpg – Downloaded images for each article (if found)

### 5. Sample Output (translation_log.txt)

Translation Log generated at 2025-07-03 21:30:00
================================================
✅ API RESPONSE: {'Translated Title': 'Spain's Democracy Faces Crisis'}
✅ API RESPONSE: {'Translated Content': 'Recent events have pushed the public...'}
...
Repeated Meaningful Words:
democracy: 3
government: 2
spain: 2


📌 Author
Renjith R.
Automation QA Engineer
