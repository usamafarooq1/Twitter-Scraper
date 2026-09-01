import os
import logging
from dotenv import load_dotenv
from src.scraper.browser_engine import AutomatedBrowserEngine
from src.exporter.storage_sink import StorageSink

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

load_dotenv()
USERNAME = os.getenv("X_USERNAME", "")
PASSWORD = os.getenv("X_PASSWORD", "")
TARGET_URL = os.getenv("TARGET_PROFILE_URL", "https://x.com/elonmusk")
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"

def run_pipeline():
    engine = AutomatedBrowserEngine(headless=HEADLESS)
    try:
        if engine.authenticate(USERNAME, PASSWORD):
            data = engine.scrape_feed(TARGET_URL, max_scrolls=10)
            StorageSink.export_to_parquet_and_csv(data)
    finally:
        engine.close()

if __name__ == "__main__":
    run_pipeline()