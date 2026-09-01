# ⚡ X (Twitter) Social Intelligence & Ingestion Engine

An automated browser ingestion engine built with Selenium 4, Pydantic, and Pandas to extract, parse, deduplicate, and persist structured microblog data into multi-format analytical sinks (CSV, Parquet).

---

## 🏗️ Architecture & Features

* **Anti-Bot & Dynamic Pagination**: Chromium automation engine with custom headers, explicit wait barriers, and dynamic scroll handling.
* **Schema Validation**: Pydantic dataclass validation ensuring strict data typing across posts, metadata, media links, and timestamps.
* **Dual Persistence Sink**: High-efficiency analytical storage in Parquet and CSV.
* **Modular Pipeline Design**: Clean separation between session authentication, DOM extraction, data parsing, and storage sinks.

---

## 🛠️ Tech Stack

* **Language**: Python 3.10+
* **Browser Automation**: Selenium 4 (Native Driver Manager)
* **Data Processing & Storage**: Pandas, PyArrow (Parquet)
* **Data Validation**: Pydantic v2
* **Configuration**: Python-Dotenv

---

## ⚙️ Quickstart Setup

### 1. Install Dependencies
```bash
py -m pip install -r requirements.txt
2. Configure Credentials
Update .env with your login credentials and target profile:

Code snippet
X_USERNAME=your_username
X_PASSWORD=your_password
TARGET_PROFILE_URL=[https://x.com/elonmusk](https://x.com/elonmusk)
HEADLESS=false
3. Run Pipeline
Bash
py main.py