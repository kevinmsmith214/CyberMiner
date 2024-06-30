import requests
from bs4 import BeautifulSoup

def fetch_urls_from_search(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    urls = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href.startswith('/url?q='):
            urls.append(href.split('/url?q=')[1].split('&sa=')[0])


    
    return urls

fetch_urls_from_search("Godzilla")