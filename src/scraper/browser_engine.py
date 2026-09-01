import time
import logging
from typing import List, Set
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.parser.tweet_extractor import TweetParser, TweetRecord

logger = logging.getLogger(__name__)

class AutomatedBrowserEngine:
    def __init__(self, headless: bool = False):
        options = Options()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 20)

    def authenticate(self, username: str, password: str) -> bool:
        logger.info("Opening login portal...")
        self.driver.get("https://x.com/i/flow/login")

        try:
            user_field = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]')))
            user_field.send_keys(username)
            user_field.send_keys(Keys.RETURN)

            pass_field = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
            pass_field.send_keys(password)
            pass_field.send_keys(Keys.RETURN)

            self.wait.until(EC.url_contains("home"))
            logger.info("Authentication complete.")
            return True
        except Exception as e:
            logger.error(f"Login failed: {e}")
            return False

    def scrape_feed(self, profile_url: str, max_scrolls: int = 15) -> List[TweetRecord]:
        self.driver.get(profile_url)
        time.sleep(3)

        records: List[TweetRecord] = []
        seen_signatures: Set[str] = set()
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        for scroll_idx in range(1, max_scrolls + 1):
            articles = self.driver.find_elements(By.CSS_SELECTOR, 'article[data-testid="tweet"]')
            for art in articles:
                parsed = TweetParser.parse_element(art)
                if parsed:
                    signature = f"{parsed.post_url}_{parsed.text[:20]}"
                    if signature not in seen_signatures:
                        seen_signatures.add(signature)
                        records.append(parsed)

            self.driver.execute_script("window.scrollBy(0, 2200);")
            time.sleep(2.5)

            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        return records

    def close(self):
        self.driver.quit()