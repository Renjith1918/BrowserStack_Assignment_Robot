from robot.api.deco import keyword
import requests
from collections import Counter
import re
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from datetime import datetime
import json
import os
import urllib.request

nltk.download('stopwords', quiet=True)

# Assigning the path to outputfiles if not create new directory
output_dir = os.path.join(os.path.dirname(__file__), "../outputfiles")
os.makedirs(output_dir, exist_ok=True)
log_file_path = os.path.join(output_dir, "translation_log.txt")
# Assigning the images path if not create new directory
image_dir = os.path.join(os.path.dirname(__file__), "../outputfiles", "images")
os.makedirs(image_dir, exist_ok=True)

# Full path to the log file
log_file_path = os.path.join(output_dir, "translation_log.txt")
# Load config
with open(os.path.join(os.path.dirname(__file__), '../config/config.json'), encoding='utf-8') as f:
    CONFIG = json.load(f)

API_KEY = CONFIG["API_KEY"]
API_HOST = CONFIG["API_HOST"]
API_URL = CONFIG["API_URL"]
HEADERS = {
    "Content-Type": "application/json",
    "X-RapidAPI-Host": API_HOST,
    "X-RapidAPI-Key": API_KEY
}

@keyword
def get_browserstack_url():
    return CONFIG["REMOTE_URL"]

@keyword
def scrape_and_translate_articles():
    stopwords_en = set(stopwords.words('english'))
    api_log_lines = []

    # Timestamp header
    timestamp = datetime.now().strftime("Translation Log generated at %Y-%m-%d %H:%M:%S")
    api_log_lines.append(timestamp)
    api_log_lines.append("=" * len(timestamp))

    def translate_text(text, label):
        try:
            payload = {
                "from": "es",
                "to": "en",
                "text": text
            }
            res = requests.post(API_URL, headers=HEADERS, json=payload)
            res.raise_for_status()
            result = res.json()
            translated = result.get("trans", "")

            log_line = f"✅ API RESPONSE: {{'Translated {label}': '{translated}'}}"
            api_log_lines.append(log_line)
            return translated

        except Exception as e:
            error_line = f"❌ Translation failed for {label}: {text[:50]}... Reason: {e}"
            api_log_lines.append(error_line)
            return ""

    try:
        response = requests.get("https://elpais.com/opinion/")
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        articles = []
        article_tags = soup.select('article')[:5]


        for idx, tag in enumerate(article_tags):
            title_tag = tag.find(['h2', 'h3'])
            content_tag = tag.find('p')
            img_tag = tag.find('img')

            if title_tag and content_tag:
                title = title_tag.get_text(strip=True)
                content = content_tag.get_text(strip=True)

                # ✅ Download image using user-agent
                if img_tag and img_tag.get("src"):
                    try:
                        image_url = img_tag["src"]
                        image_path = os.path.join(image_dir, f"article_{idx+1}.jpg")

                        req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
                        with urllib.request.urlopen(req) as resp, open(image_path, 'wb') as out_file:
                            out_file.write(resp.read())
                    except Exception as e:
                        print(f"❌ Failed to download image for article {idx+1}: {e}")

                articles.append({"title": title, "content": content})

        translated = []
        translated_word_list = []

        for article in articles:
            title = article["title"]
            content = article["content"]

            translated_title = translate_text(title, "Title")
            translated_content = translate_text(content, "Content")

            combined_text = f"{translated_title} {translated_content}"
            words = re.findall(r"\b\w{3,}\b", combined_text.lower())
            words = [w for w in words if w not in stopwords_en]
            translated_word_list.extend(words)

            translated.append({
                "original_title": title,
                "original_content": content,
                "translated_title": translated_title,
                "translated_content": translated_content
            })

        word_freq = Counter(translated_word_list)
        repeated_words = {word: count for word, count in word_freq.items() if count > 1}

        api_log_lines.append("\nRepeated Meaningful Words:")
        for word, count in sorted(repeated_words.items(), key=lambda x: x[1], reverse=True):
            api_log_lines.append(f"{word}: {count}")

        with open(log_file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(api_log_lines))
        return translated, repeated_words

    except Exception as e:
        error = f"❌ Error during scraping and translation: {e}"
        with open(log_file_path, "w", encoding="utf-8") as f:
            f.write(error + "\n")
        return [], {}

