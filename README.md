
# 🕵️ Ultimate Business Lead Scraper

This is a powerful, end-to-end scraper for collecting business leads such as name, email, phone number, address, and website from YellowPages and other sources. It supports multiple business categories and uses a hybrid approach combining Selenium and HTTP requests.

---

## 🚀 Features

- 🔎 Scrapes businesses by category and location (city, state)
- 🧠 Extracts **emails**, **phone numbers**, **websites**, and **addresses**
- 🧰 Uses **Selenium** to handle dynamic web pages
- 🌐 **Enhances data** using Google search when email is not found
- 🤖 **Fake User-Agent rotation** to avoid detection
- ✅ Saves leads into **formatted Excel (.xlsx)** files
- 🛡️ Smart error handling and deduplication

---

## 🛠️ Requirements

- Python 3.7+
- Google Chrome installed
- [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/) installed and its path set in the script

### Install dependencies

```bash
pip install selenium beautifulsoup4 pandas openpyxl fake-useragent requests
```

---

## 🧪 How to Use

1. Update the ChromeDriver path in `CHROMEDRIVER_PATH` (default: `C:/WebDriver/chromedriver.exe`).
2. Run the script:

```bash
python ultimate_scraper.py
```

3. Input the **City** and **State Abbreviation** when prompted.
4. Sit back and let the scraper do its job.
5. Collected leads will be saved in Excel files named like: `Cleaning_Los_Angeles_CA.xlsx`

---

## 🧱 Tech Stack

- `Selenium` – for browser automation
- `BeautifulSoup` – for parsing HTML content
- `pandas` + `openpyxl` – for Excel export
- `requests` – for HTTP data enrichment
- `fake-useragent` – for random User-Agent headers

---

## 📁 Output Format

Each row in the Excel file contains:

| Name | Phone | Email | Website | Address |
|------|-------|--------|---------|---------|

---

## 📌 Notes

- Avoid scraping too fast to prevent being blocked.
- Results depend on YellowPages listings and Google visibility.
- This script does not scrape Yelp/Crunchbase due to CAPTCHA restrictions.

---

## 📃 License

MIT License – free to use, modify, and distribute.

---

## 🙌 Acknowledgments

Made by combining and polishing multiple scraping techniques to create a powerful lead generation tool.
