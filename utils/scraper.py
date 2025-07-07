from robot.api.deco import keyword
from datetime import datetime
import requests
from collections import Counter
import re
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
import json
import os
import urllib.request
from robot.api import logger
import time
from SeleniumLibrary import SeleniumLibrary
from robot.libraries.BuiltIn import BuiltIn


nltk.download('stopwords', quiet=True)


@keyword(name="Navigate To Opinion Section")
def navigate_to_opinion_section(url):
    sl = BuiltIn().get_library_instance("SeleniumLibrary")
    sl.go_to(url)
    try:
        sl.wait_until_element_is_visible("xpath=//*[@id='didomi-notice-agree-button']", timeout="10s")
        sl.scroll_element_into_view("xpath=//*[@id='didomi-notice-agree-button']")
        sl.click_element("xpath=//*[@id='didomi-notice-agree-button']")
    except Exception as e:
        BuiltIn().log(f"Consent button not clickable: {e}", level="WARN")

    time.sleep(2)
    page_source = sl.get_source()
    return BeautifulSoup(page_source, "html.parser")

@keyword(name="Fetch Top Articles")
def fetch_top_articles(soup, count):
    count = int(count)
    article_tags = soup.select('article')[:count]
    articles = []
    for tag in article_tags:
        title_tag = tag.find(['h2', 'h3'])
        content_tag = tag.find('p')
        img_tag = tag.find('img')
        if title_tag and content_tag:
            title = title_tag.get_text(strip=True)
            content = content_tag.get_text(strip=True)
            image_url = img_tag['src'] if img_tag and img_tag.get('src') else None
            articles.append({"title": title, "content": content, "image_url": image_url})
    return articles

@keyword(name="Print Articles In Spanish")
def print_articles_in_spanish(articles):
    for a in articles:
        print(f"{a['title']}\n{a['content']}\n")

@keyword(name="Download Cover Images")
def download_cover_images(articles, platform, timestamp=None):
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder_name = f"{platform}_{current_time}"
    image_dir = os.path.join(os.path.dirname(__file__), f"../results/image/{folder_name}")
    os.makedirs(image_dir, exist_ok=True)
    for idx, article in enumerate(articles):
        if article.get("image_url"):
            try:
                image_path = os.path.join(image_dir, f"article_{idx+1}.jpg")
                req = urllib.request.Request(article["image_url"], headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req) as resp, open(image_path, 'wb') as out_file:
                    out_file.write(resp.read())
            except Exception as e:
                print(f"❌ Failed to download image {idx+1}: {e}")


@keyword(name="Translate Article Titles")
def translate_article_titles(articles):
    CONFIG = json.load(open(os.path.join(os.path.dirname(__file__), '../config/config.json'), encoding='utf-8'))
    API_URL = CONFIG["API_URL"]
    HEADERS = {
        "Content-Type": "application/json",
        "X-RapidAPI-Host": CONFIG["API_HOST"],
        "X-RapidAPI-Key": CONFIG["API_KEY"]
    }
    translated = []
    for a in articles:
        payload = {"from": "es", "to": "en", "text": a["title"]}
        try:
            r = requests.post(API_URL, headers=HEADERS, json=payload)
            r.raise_for_status()
            json_response = r.json()
            trans = json_response.get("trans", "")
            if not trans:
                logger.warn(f"No translation returned for: {a['title']}")
        except Exception as e:
            logger.error(f"Translation failed for '{a['title']}': {e}")
            trans = ""
        translated.append({**a, "translated_title": trans})
    return translated

@keyword(name="Analyze Repeated Words In Titles")
def analyze_repeated_words_in_titles(articles):
    stopwords_en = set(stopwords.words('english'))
    words = []
    for a in articles:
        text = a.get("translated_title", "")
        words.extend([w for w in re.findall(r"\b\w{3,}\b", text.lower()) if w not in stopwords_en])
    counter = Counter(words)
    return {k: v for k, v in counter.items() if v > 1}

@keyword(name="Log Translation Results")
def log_translation_results(articles, repeated, platform, timestamp=None):
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder_name = f"{platform}_{current_time}"
    log_dir = os.path.join(os.path.dirname(__file__), f"../results/translation_log/{folder_name}")
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "translation_log.txt")
    lines = []
    lines.append(f"Translation log generated at {current_time}")
    lines.append("-----------------------------------------------\n")
    lines.append("First five articles in Opinion")
    lines.append("==============================\n")
    for idx, a in enumerate(articles, 1):
        lines.append(f"Title{idx} (Spanish): {a['title']}")
        lines.append(f"Content (Spanish): {a['content']}\n")
    lines.append("\nTranslated Titles (English):")
    lines.append("==============================\n")
    for idx, a in enumerate(articles, 1):
        lines.append(f"Translated Title{idx}: {a.get('translated_title', '')}")
    lines.append("\n\nRepeated Words in Titles:")
    lines.append("==============================")
    if repeated:
        for word, count in repeated.items():
            lines.append(f"{word}: {count}")
    else:
        lines.append("No Repeated Words in Titles")
    log_content = "\n".join(lines)
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write(log_content)
    logger.info(f"\n--- Translation Log for {platform} ---\n{log_content}")
