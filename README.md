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

To run test locally in single platform:
**robot --outputdir Singlerun .\tests\test_elpais.robot**

To run test parallelly in five platforms across a combination of desktop and mobile browsers:
**python parallel_runner.py**

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
2. images/article_0.jpg to article_4.jpg – Downloaded images for each article (if found).
3. In case of parallel run, individual results,images and translation logs are generated in the respective platform folders.

### 5. Sample Output (translation_log.txt)

Translation log generated at 2025-07-06_22-16-47
-----------------------------------------------

First five articles in Opinion
==============================

Title1 (Spanish): Respuesta insuficiente
Content (Spanish): Las medidas anunciadas por Pedro Sánchez ante el PSOE no cierran la crisis de credibilidad generada por el ‘caso Cerdán’

Title2 (Spanish): El abuelo enterrado en el jardín
Content (Spanish): A medida que Putin necesite a Stalin como héroe de la Segunda Guerra Mundial, irán apareciendo más estatuas suyas

Title3 (Spanish): Las mujeres primero
Content (Spanish): Creo en un cambio de sistema en el que nosotras tengamos voz para señalar el curso del mundo

Title4 (Spanish): Incertidumbre
Content (Spanish): Hace apenas dos siglos que los seres humanos adquirimos la conciencia de que en el plazo de nuestra existencia podíamos vivir en varios estadios históricos. Hoy todo se ha acelerado

Title5 (Spanish): Por quién cantan las sirenas
Content (Spanish): El delta de la Camarga, a menudo idealizado como un refugio natural salvaje, ha sido moldeado durante siglos por el ser humano para hacerlo habitable. Según una herramienta del IPCC, con un aumento de 2,5°C, gran parte del delta del Ródano quedaría sumergido. Localidades como Aigues-Mortes y Arlés estarían bajo el agua o junto al mar. Para comprender cómo enfrentan los habitantes este futuro incierto, el autor se adentra en sus vidas: personas arraigadas a tradiciones rurales, rebeldes, de caza y agricultura. A través de retratos y reflexiones poéticas, el texto retrata un territorio y a sus gentes ante la amenaza de desaparecer


Translated Titles (English):
==============================

Translated Title1: Insufficient response
Translated Title2: The grandfather buried in the garden
Translated Title3: Women first
Translated Title4: Uncertainty
Translated Title5: For whom the sirens sing


Repeated Words in Titles:
==============================
No Repeated Words in Titles


📌 Author
Renjith R.
Automation QA Engineer
