import requests
from bs4 import BeautifulSoup

def scrape(url):
    '''Scrapes data from url'''
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def find_links(soup):
    '''Finds links of all <a> tags with class "card__title-link" and returns the href attribute of each found element'''
    hrefs = []
    links = soup.find_all('a', class_='card__title-link')
    for link in links:
        hrefs.append(link['href'])
    return hrefs

def scrape_multiple_pages(base_url, total_pages):
    '''Scrapes multiple pages and collects all the links'''
    all_links = []
    for page_num in range(1, total_pages + 1):
        url = f"{base_url}&page={page_num}"
        soup = scrape(url)
        page_links = find_links(soup)
        all_links.extend(page_links)
    return all_links


buy = []

base_url = "https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&priceType=SALE_PRICE&page=1&orderBy=relevance"
total_pages = 333


all_links = scrape_multiple_pages(base_url, total_pages)


for link in all_links:
    buy.append(link)

buy_set = set(buy)
print(buy_set)
print(len(buy_set))