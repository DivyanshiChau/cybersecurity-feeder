import requests
import ssl
import socket
import json
import os
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pymongo import MongoClient  # MongoDB client
from webdriver_manager.chrome import ChromeDriverManager  
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def is_https(url):
    """Check if the URL uses HTTPS."""
    return url.startswith('https://')

def is_ssl_certificate_valid(url):
    """Check if the SSL certificate of the URL is valid."""
    try:
        parsed_url = requests.utils.urlparse(url)
        hostname = parsed_url.hostname
        port = parsed_url.port or 443
        context = ssl.create_default_context()
        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                ssock.getpeercert()
        return True
    except Exception as e:
        print(f"SSL certificate validation failed: {e}")
        return False

def fetch_cyware_data():
    """Scrape news articles from Cyware and return the data."""
    url = "https://cyware.com/search?search=india"

    
    if not is_https(url):
        return {"error": "URL does not use HTTPS."}
    if not is_ssl_certificate_valid(url):
        return {"error": "SSL certificate is not valid."}
    
    
    chrome_options = Options()
    
    chrome_options.add_argument("--no-sandbox")  
    chrome_options.add_argument("--disable-dev-shm-usage")  
    
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'cy-card')]"))
    )

    articles = driver.find_elements(By.XPATH, "//div[contains(@class, 'cy-panel') and contains(@class, 'cy-card')]")
    print(f"Found {len(articles)} articles.") 

    news_data = []

    
    for article in articles:
        try:
            title = article.find_element(By.CLASS_NAME, "cy-card__title").text.strip() if article.find_elements(By.CLASS_NAME, "cy-card__title") else "No Title"
            summary = article.find_element(By.CLASS_NAME, "cy-card__description").text.strip() if article.find_elements(By.CLASS_NAME, "cy-card__description") else "No Summary"
            link = article.find_element(By.TAG_NAME, "a").get_attribute("href") if article.find_elements(By.TAG_NAME, "a") else "No Link"
            date_elements = article.find_elements(By.CLASS_NAME, "cy-card__meta")
            date = next((elem.text.strip() for elem in date_elements if re.match(r'\w+ \d{1,2}, \d{4}', elem.text.strip())), "No Date")
            news_item = {
                "title": title,
                "summary": summary,
                "link": link,
                "date": date
            }

            
            news_data.append(news_item)
        except Exception as e:
            print(f"Error extracting data from article: {e}")

    
    driver.quit()

    if not news_data:
        print("No data was scraped.")
    else:
        print(f"Successfully scraped {len(news_data)} articles.")
    
    return news_data

def save_data_to_json(news_data):
    """Save the scraped data to a JSON file on the desktop."""
   
    

    relative_folder_path = os.path.join(os.path.dirname(__file__), "fetched_data")
   
    
    json_file_path = os.path.join(relative_folder_path, "cyware_news.json")

    with open(json_file_path, "w") as json_file:
        json.dump(news_data, json_file, indent=4, separators=(',', ': '))
    
    print(f"Data saved to {json_file_path}")

def save_data_to_mongodb(news_data):
    """Insert the scraped data into MongoDB."""
    # Connect to MongoDB 
    client = MongoClient("mongodb://localhost:27017/")  # Update with MongoDB URI if different
    db = client["cyber_news_db"]  # Create/use a database named "cyber_news_db"
    collection = db["cyware_news"]  # Create/use a collection named "cyware_news"

    
    if news_data:  
        collection.insert_many(news_data)
        print("Data inserted into MongoDB.")

def main():
    """Main function to run the scraping, saving, and database insertion."""
    print("Starting data scraping from Cyware...")
    
   
    news_data = fetch_cyware_data()

    if "error" in news_data:
        print(news_data["error"])
        return
    
    save_data_to_json(news_data)
    save_data_to_mongodb(news_data)

    print("Scraping completed, data saved to JSON file and inserted into MongoDB.")

if __name__ == "__main__":
    main()
