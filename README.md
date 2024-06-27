# Twitter-Scraper

## Description
Twitter-Scraper is a general-purpose scraper that automates the extraction of tweets from any specified Twitter profile or search results using Python and Selenium. The script handles login, navigation, scrolling, and data collection, including tweet text, dates, links, and images. The collected data is saved into an Excel file for further analysis.

## Features
- **Automated Login**: Logs into Twitter with provided credentials.
- **Data Extraction**: Extracts tweet text, timestamps, external links, and images.
- **Continuous Scrolling**: Scrolls through the Twitter page to load and collect more tweets.
- **State Persistence**: Saves the state periodically to resume from the last saved state in case of interruptions.
- **Data Storage**: Saves the collected tweets into an Excel file.

## Requirements
- Python 3.x
- Selenium
- Pandas
- WebDriver Manager for Chrome
- Dateutil

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/twitter-scraper.git
    cd twitter-scraper
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Ensure you have Chrome browser installed and a compatible ChromeDriver.

## Usage
1. Update the script with your Twitter login credentials:
    ```python
    username_str = "your_username"
    password_str = "your_password"
    ```

2. Set the target URL for scraping (profile or search result):
    ```python
    url = "https://twitter.com/some_profile_or_search_query"
    ```

3. Run the script:
    ```sh
    python twitter_scraper.py
    ```

4. The script will log into Twitter, navigate to the specified URL, scroll through the page, and save the collected tweets into `tweets.xlsx`.

## Code Overview
```python
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager as CM
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from dateutil.parser import parse
import pickle
import os.path

# Twitter login credentials
username_str = "your_username"
password_str = "your_password"

# Set up Chrome options
options = Options()
options.add_argument("--start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_argument("--headless")

# Initialize the Chrome WebDriver
service = Service(executable_path=CM().install())
driver = webdriver.Chrome(service=service, options=options)

# Open Twitter login page
url = "https://twitter.com/i/flow/login"
driver.get(url)

try:
    # Wait for the username input and enter the username
    username = WebDriverWait(driver, 60).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]')))
    username.send_keys(username_str)
    username.send_keys(Keys.RETURN)

    # Wait for the password input and enter the password
    password = WebDriverWait(driver, 60).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
    password.send_keys(password_str)
    password.send_keys(Keys.RETURN)

    # Wait for the profile page to load after login
    time.sleep(25)

    # Open the Twitter profile page
    driver.get("https://x.com/madatcommunity")

    # Wait for the page to load
    time.sleep(25)
except TimeoutException:
    print("Loading took too much time!")
    driver.quit()
    exit()

# Scroll the page to load more tweets
scroll_pause_time = 15  # Reduced scroll pause time for more frequent scrolling

new_height = 0
last_height = driver.execute_script("return window.pageYOffset;")
scrolling = True
# Initialize scrolling variables
scroll_count = 0
tweets_collected = set()  # Use a set to avoid duplicates
tweets_data = []  # List to store tweet data

# Function to extract digits from a string (not used in this version of the script)
def extract_digits(text):
    return int(''.join(filter(str.isdigit, text)))

# Load previous state from pickle file if exists
scroll_state_file = "scroll_state.pkl"
if os.path.exists(scroll_state_file):
    with open(scroll_state_file, "rb") as f:
        try:
            scroll_count, last_height, tweets_collected, tweets_data = pickle.load(f)
            print("Resumed from previous state.")
        except Exception as e:
            print(f"Error loading state from {scroll_state_file}: {e}")
            print("Starting fresh.")
else:
    print("No previous state found. Starting fresh.")

# Function to save current state to pickle file
def save_state():
    with open(scroll_state_file, "wb") as f:
        pickle.dump((scroll_count, last_height, tweets_collected, tweets_data), f)

while True:  # Infinite loop for continuous scrolling
    try:
        tweets = driver.find_elements(By.CSS_SELECTOR, 'article[data-testid="tweet"]')

        for tweet in tweets:
            try:
                tweet_text = tweet.find_element(By.CSS_SELECTOR, 'div[lang]').text
            except NoSuchElementException:
                tweet_text = ""
                print("No tweet text found")

            try:
                timestamp = tweet.find_element(By.TAG_NAME, "time").get_attribute("datetime")
                tweet_date = parse(timestamp).isoformat().split("T")[0]
            except Exception as ex:
                tweet_date = ""
                print(f"Error parsing date: {ex}")

            try:
                anchor = tweet.find_element(By.CSS_SELECTOR, "a[aria-label][dir]")
                external_link = anchor.get_attribute("href")
            except Exception as ex:
                external_link = ""
                print(f"Error finding external link: {ex}")

            try:
                images = tweet.find_elements(By.CSS_SELECTOR, 'div[data-testid="tweetPhoto"] img')
                tweet_images = [img.get_attribute("src") for img in images]
            except Exception as ex:
                tweet_images = []
                print(f"Error finding images: {ex}")

            images_links = ', '.join(tweet_images) if tweet_images else "No Images"

            if (tweet_text, tweet_date, external_link, images_links) not in tweets_collected:
                tweets_collected.add((tweet_text, tweet_date, external_link, images_links))
                tweets_data.append((tweet_text, tweet_date, external_link, images_links))
                print(
                    f"Date: {tweet_date}, Tweet: {tweet_text}, Link: {external_link}, Images: {images_links}")

        # Scroll down
        driver.execute_script("window.scrollBy(0, 1500);")
        time.sleep(scroll_pause_time)

        # Update heights
        new_height = driver.execute_script("return document.body.scrollHeight")
        print(f"Scroll count: {scroll_count}, New height: {new_height}, Last height: {last_height}")

        # Check if scrolling is stuck
        if new_height == last_height:
            print("Scrolling stuck, waiting...")
            time.sleep(scroll_pause_time * 3)  # Wait longer to see if page loads
            new_height = driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                print("Scrolling still stuck, attempting to break...")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(scroll_pause_time * 5)  # Wait and attempt to scroll down again
                new_height = driver.execute_script("return document.body.scrollHeight")

                if new_height == last_height:
                    print("Again Scrolling still stuck, attempting to break...")
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(scroll_pause_time * 10)  # Wait and attempt to scroll down again
                    new_height = driver.execute_script("return document.body.scrollHeight")

                    if new_height == last_height:
                        print("Scrolling broken, exiting...")
                        break

        last_height = new_height
        scroll_count += 1

        # Save state periodically
        if scroll_count % 10 == 0:  # Adjust frequency of state saving as needed
            save_state()

    except WebDriverException as e:
        print(f"An error occurred during scraping: {e}")
        break

# Close the browser
driver.quit()

# Create a DataFrame and save it to an Excel file
df = pd.DataFrame(tweets_data, columns=["Tweet", "Date", "Link", "Images"])
df.to_excel("tweets.xlsx", index=False)

# Print the total number of tweets collected
print(f"Total tweets collected: {len(tweets_data)}")

# Delete the scroll state file after successful scraping (optional)
if os.path.exists(scroll_state_file):
    os.remove(scroll_state_file)

print("Script execution completed.")
