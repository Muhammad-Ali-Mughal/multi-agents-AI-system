import os
from dotenv import load_dotenv

from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import tool
import requests

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from readability import Document
import trafilatura
import re

load_dotenv()

web_search_tool = DuckDuckGoSearchRun()

result = web_search_tool.invoke("What is the capital of France?")

def scrape_url(url: str) -> dict:
    # Open website in a browser
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        html = page.content()

        browser.close()

    # Detect blocked pages
    if "Enable JavaScript and cookies to continue" in html:
        raise RuntimeError("Website requires browser verification.")

    # Extract title
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.get_text(strip=True) if soup.title else ""

    # Extract main content
    content = trafilatura.extract(html)

    if not content:
        readable_html = Document(html).summary()
        content = BeautifulSoup(
            readable_html, "html.parser"
        ).get_text(separator="\n", strip=True)

    content = re.sub(r"\n{3,}", "\n\n", content or "").strip()

    print(f"Scraped URL: {url}, Title: {title}, Content Length: {content}")

    return {
        "url": url,
        "title": title,
        "content": content
    }