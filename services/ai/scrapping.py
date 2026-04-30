import time
from urllib.parse import urlparse

from bs4 import BeautifulSoup
import cloudscraper

from services.ai.personas import cookai_client, make_scrapping_prompt
from services.ai.extract_fields import extract_title
from settings.settings import GENAI_MODEL


def scrap_recipe(url: str) -> dict:
    start_time = time.time()
    parsed_url = urlparse(url)
    font_of_url = parsed_url.netloc

    scraper = cloudscraper.create_scraper()

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        response = scraper.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        for script in soup(["script", "style"]):
            script.decompose()

        text = soup.get_text(separator="\n", strip=True)

        prompt_content = make_scrapping_prompt(text, font_of_url)
        response = cookai_client.models.generate_content(
            model=GENAI_MODEL, contents=prompt_content
        )

        title = extract_title(response.text)
        return {
            "title": title or "Untitled",
            "content": response.text,
            "font": font_of_url,
            "link": url,
            "duration_ms": int((time.time() - start_time) * 1000),
        }
    except Exception as error:
        return {"error": f"Failed to scrape recipe: {error}"}
