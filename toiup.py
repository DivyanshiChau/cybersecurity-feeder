import os
import json
import requests
from bs4 import BeautifulSoup
url = "https://timesofindia.indiatimes.com/topic/Cyber-crime/news"

output_dir = "fetched_data"
os.makedirs(output_dir, exist_ok=True)  
try:
    response = requests.get(url, verify=True)
    response.raise_for_status()
   
    soup = BeautifulSoup(response.content, 'html.parser')
    
    news_data = []
    articles = soup.find_all("div", class_="uwU81")
    for article in articles:
        title = article.find("div", class_="fHv_i").text.strip() if article.find("div", class_="fHv_i") else None
        summary = article.find("p", class_="oxXSK o58kM").text.strip() if article.find("p", class_="oxXSK o58kM") else None
        link = article.find("a")['href'] if article.find("a") else None
        if link and not link.startswith('http'):
            link = "https://timesofindia.indiatimes.com" + link  
        source_date = article.find("div", class_="ZxBIG").text.strip() if article.find("div", class_="ZxBIG") else None
        author, date = None, None
        if source_date:
            parts = source_date.split('/')
            author = parts[0].strip() if len(parts) > 1 else None
            date = parts[1].strip() if len(parts) > 1 else source_date
        
        news_item = {
            "title": title,
            "summary": summary,
            "link": link,
            "author": author,
            "date": date
        }
        news_data.append(news_item)

    output_path = os.path.join(output_dir, "cybersecurity_news.json")
    with open(output_path, "w") as json_file:
        json.dump(news_data, json_file, indent=4, separators=(',', ': '))

    print(f"Scraping completed and data saved to {output_path}")

except requests.RequestException as e:
    print(f"Failed to retrieve the page. Error: {e}")
