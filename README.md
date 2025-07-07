# El País Opinion Scraper & Translator (Robot Framework)

This Robot Framework automation project performs end-to-end scraping, translation, and analysis of articles from the *Opinion* section of [https://elpais.com/], a leading Spanish news outlet.

-----------------------------------------------------------------------

📌 Overview
1. Scrapes the top 5 opinion articles from El País
2. Extracts titles, content, and downloads cover images (if available)
3. Translates titles and content using Google Translate API (RapidAPI)
4. Analyzes translated content for repeated keywords
5. Supports local execution and parallel BrowserStack testing

✅ Features
1. Opens El País Opinion section remotely via BrowserStack
2. Handles cookie consent popup if it appears
3. Extracts titles and content of top 5 articles
4. Translates Spanish content into English via RapidAPI
5. Downloads article images (if available)
6. Analyzes repeated meaningful words in titles
7. Generates translation_log.txt for logs and insights
8. Supports both local and parallel cross-browser testing

⚙️ Setup Instructions
1. 📦 Install Dependencies
Ensure you have Python 3.7+ installed.

Install required dependencies:
**pip install -r requirements.txt**

2. 🔐 Configure Credentials
Edit config/config.json with your credentials:

{
  "URL": "https://elpais.com/opinion/",
  "API_KEY": "<your_rapidapi_key>",
  "API_HOST": "google-translate113.p.rapidapi.com",
  "API_URL": "https://google-translate113.p.rapidapi.com/api/v1/translator/text",
  "REMOTE_URL": "https://<user_name>:<access_key>@hub-cloud.browserstack.com/wd/hub",
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

🚀 How to Run Tests
➤ To run locally (default browser):

**robot --outputdir reports/log_local_run tests/test_elpais.robot**

✅ This will:
1. Launch Chrome locally
2. Navigate to El País Opinion section
3. Scrape, translate, download images
4. Save logs and outputs under reports/log_local_run/

➤ To run on BrowserStack (parallel execution):

**python parallel_runner.py**

✅ This will:
1. Launch tests on 5 different BrowserStack platforms (configurable)
2. Perform scraping, translation, and analysis
3. Save platform-specific outputs under reports/logs_<platform>_run/

📂 Output Files:

1.reports will be stored under
\reports\log_<platform>_run

2.Images will be stored under
\results\image\<platform>_CurrentTime

3.Translated files(.txt) will be stored under
\results\translation_log\<platform>_CurrentTime

📄 Sample Output (translation_log.txt)

Translation log generated at 2025-07-07_13-43-51
-----------------------------------------------

First five articles in Opinion
==============================

Title1 (Spanish): Un PP atado a Vox
Content (Spanish): Feijóo consigue que el congreso del popular cierre filas con él, pero su dependencia de la formación ultra contradice sus ansias centristas

Title2 (Spanish): Respuesta insuficiente
Content (Spanish): Las medidas anunciadas por Pedro Sánchez ante el PSOE no cierran la crisis de credibilidad generada por el ‘caso Cerdán’

Title3 (Spanish): Un putero representa todos los errores de la historia
Content (Spanish): La guerra, el imperialismo, el robo más sucio y la emergencia climática guardan un nexo común: la misoginia

Title4 (Spanish): Nuestra mente está en guerra
Content (Spanish): La insistencia en la necesidad del debate de ideas no es intelectualismo nostálgico, nos va la vida en ello

Title5 (Spanish): Por quién cantan las sirenas
Content (Spanish): El delta de la Camarga, a menudo idealizado como un refugio natural salvaje, ha sido moldeado durante siglos por el ser humano para hacerlo habitable. Según una herramienta del IPCC, con un aumento de 2,5°C, gran parte del delta del Ródano quedaría sumergido. Localidades como Aigues-Mortes y Arlés estarían bajo el agua o junto al mar. Para comprender cómo enfrentan los habitantes este futuro incierto, el autor se adentra en sus vidas: personas arraigadas a tradiciones rurales, rebeldes, de caza y agricultura. A través de retratos y reflexiones poéticas, el texto retrata un territorio y a sus gentes ante la amenaza de desaparecer


Translated Titles (English):
==============================

Translated Title1: A PP tied to Vox
Translated Title2: Insufficient response
Translated Title3: A whore represents all the mistakes of history
Translated Title4: Our mind is at war
Translated Title5: For whom the sirens sing


Repeated Words in Titles:
==============================
No Repeated Words in Titles






----------------------------
👨‍💻 Author

Renjith R.

Automation QA Engineer

renjith.official326@gmail.com