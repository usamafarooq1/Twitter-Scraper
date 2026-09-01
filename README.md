# 🐦 Twitter / X Data Scraper & Data Harvester For Reseachers

An open-source, automated scraper and data ingestion tool built with Python, Selenium, and Pandas. Designed for academic researchers, data journalists, and analysts to collect, parse, and export structured tweet datasets (CSV / Parquet / Excel) without relying on expensive API tiers.

---

## 🎯 Use Cases for Research

* **Academic & Social Science Research**: Collect public discourse datasets, hashtag trends, and public sentiment over time.
* **NLP & Text Mining**: Harvest rich conversational text corpora with timestamps and user references.
* **Media & Information Studies**: Extract post links, embedded media URLs, and publication metadata for content analysis.

---

## ✨ Features

* **No Official API Required**: Scrapes public dynamic feeds directly using browser automation.
* **Dynamic Scroll & Anti-Bot Handling**: Emulates authentic browser sessions with adaptive scrolling and explicit wait barriers.
* **Strict Schema Validation**: Validates extracted tweets with Pydantic for clean, analysis-ready datasets.
* **Multi-Format Analytical Sinks**: Persists records directly into `.csv`, `.parquet`, and `.xlsx`.
* **State Checkpointing**: Automatically caches progress during long scrapes to prevent data loss.

---

## 🛠️ Tech Stack

* **Language**: Python 3.10+
* **Automation**: Selenium 4 (Native Driver Manager)
* **Data Processing**: Pandas, PyArrow (Parquet), OpenPyXL (Excel)
* **Schema Validation**: Pydantic v2
* **Environment**: Python-Dotenv

---

## 🚀 Quickstart Guide

### 1. Clone & Install Dependencies
```bash
git clone [https://github.com/usamafarooq1/Twitter-Scraper.git](https://github.com/usamafarooq1/Twitter-Scraper.git)
cd Twitter-Scraper
py -m pip install -r requirements.txt

```

### 2. Configure Credentials

Update `.env` with your login credentials and target profile:

```env
X_USERNAME=your_username
X_PASSWORD=your_password
TARGET_PROFILE_URL=https://x.com/elonmusk
HEADLESS=false

```

### 3. Run Pipeline

```bash
py main.py

```
