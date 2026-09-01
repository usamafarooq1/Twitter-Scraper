from typing import Optional, List
from pydantic import BaseModel
from dateutil.parser import parse
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class TweetRecord(BaseModel):
    tweet_id: Optional[str] = None
    text: str
    published_date: Optional[str] = None
    post_url: Optional[str] = None
    image_urls: List[str] = []

class TweetParser:
    @staticmethod
    def parse_element(article: WebElement) -> Optional[TweetRecord]:
        try:
            try:
                text_el = article.find_element(By.CSS_SELECTOR, 'div[lang]')
                text = text_el.text.strip()
            except NoSuchElementException:
                text = ""

            try:
                time_el = article.find_element(By.TAG_NAME, "time")
                raw_time = time_el.get_attribute("datetime")
                published_date = parse(raw_time).isoformat().split("T")[0] if raw_time else None
            except Exception:
                published_date = None

            try:
                link_el = article.find_element(By.CSS_SELECTOR, 'a[href*="/status/"]')
                post_url = link_el.get_attribute("href")
            except Exception:
                post_url = None

            try:
                img_elements = article.find_elements(By.CSS_SELECTOR, 'div[data-testid="tweetPhoto"] img')
                image_urls = [img.get_attribute("src") for img in img_elements if img.get_attribute("src")]
            except Exception:
                image_urls = []

            if not text and not image_urls:
                return None

            return TweetRecord(
                text=text,
                published_date=published_date,
                post_url=post_url,
                image_urls=image_urls
            )
        except Exception:
            return None