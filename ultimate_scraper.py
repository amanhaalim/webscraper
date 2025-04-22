
import time
import re
import random
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from fake_useragent import UserAgent
import urllib.parse

CHROMEDRIVER_PATH = "C:/WebDriver/chromedriver.exe"  # Update if needed
HEADERS = {"User-Agent": "Mozilla/5.0"}

CATEGORIES = [
]

ua = UserAgent()

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=chrome_options)

def extract_emails(text):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, text)
    return [email for email in set(emails) if "noreply" not in email and "example.com" not in email]

def extract_phone(text):
    patterns = [
        r'\+1[\s.-]?\d{3}[\s.-]?\d{3}[\s.-]?\d{4}',
        r'\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}',
        r'\d{3}[\s.-]?\d{3}[\s.-]?\d{4}'
    ]
    phones = []
    for pattern in patterns:
        phones.extend(re.findall(pattern, text))
    return list(set(phones))

def enrich_google_search(business_name, location):
    try:
        query = f"{business_name} {location} contact email"
        url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
        headers = {"User-Agent": ua.random}
        response = requests.get(url, headers=headers, timeout=10)
        return extract_emails(response.text)
    except:
        return []

def scrape_yellowpages(driver, category, location):
    leads = []
    city, state = location.split(",")
    page = 1

    while True:
        url = f"https://www.yellowpages.com/search?search_terms={category.replace(' ', '+')}&geo_location_terms={location.replace(' ', '+')}&page={page}"
        driver.get(url)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        results = soup.find_all("div", class_="result")
        if not results:
            break

        for biz in results:
            try:
                name_elem = biz.find("a", class_="business-name")
                name = name_elem.text.strip() if name_elem else "N/A"

                phone_elem = biz.find("div", class_="phones phone primary")
                phone = phone_elem.text.strip() if phone_elem else "N/A"

                address_elem = biz.find("div", class_="street-address")
                locality_elem = biz.find("div", class_="locality")
                address = (address_elem.text.strip() if address_elem else "") + " " + (locality_elem.text.strip() if locality_elem else "")

                website_elem = biz.find("a", class_="track-visit-website")
                website = website_elem['href'] if website_elem else "N/A"

                emails = extract_emails(str(biz))
                if not emails:
                    emails = enrich_google_search(name, location)
                email = emails[0] if emails else "N/A"

                if name != "N/A" and email != "N/A":
                    lead = {
                        "Name": name,
                        "Phone": phone,
                        "Email": email,
                        "Website": website,
                        "Address": address.strip()
                    }
                    if not any(x['Name'] == name for x in leads):
                        leads.append(lead)
                        print(f"Added: {name} | {email} | {phone}")
            except Exception as e:
                print(f"Error: {e}")
                continue

        page += 1
        next_button = soup.find("a", class_="next")
        if not next_button:
            break

    return leads

def save_to_excel(leads, category, location):
    if not leads:
        print(f"No leads for {category} in {location}")
        return

    filename = f"{category.replace(' ', '_')}_{location.replace(', ', '_')}.xlsx"
    df = pd.DataFrame(leads)
    df.to_excel(filename, index=False)
    print(f"Saved {len(df)} leads to {filename}")

def main():
    city = input("Enter City: ").strip()
    state = input("Enter State (e.g., TX): ").strip()
    location = f"{city}, {state}"
    driver = get_driver()

    for category in CATEGORIES:
        print(f"\nScraping category: {category}")
        try:
            leads = scrape_yellowpages(driver, category, location)
            save_to_excel(leads, category, location)
        except Exception as e:
            print(f"Error scraping {category}: {e}")

    driver.quit()

if __name__ == "__main__":
    main()
