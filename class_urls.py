from bs4 import BeautifulSoup
import requests


class Urls:
    def __init__(self):
        self.urls = []

    def scrape(self, url):
        '''Scrapes data from url'''
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup

    def find_links(self, soup):
        '''Finds links of all <a> tags with class "card__title-link" and returns the href attribute of each found element'''
        hrefs = []
        links = soup.find_all('a', class_='card__title-link')
        for link in links:
            hrefs.append(link['href'])
        return hrefs

    def scrape_multiple_pages(self, base_url, total_pages):
        '''Scrapes multiple pages and collects all the links'''
        self.urls = []
        for page_num in range(1, total_pages + 1):
            url = f"{base_url}&page={page_num}"
            soup = self.scrape(url)
            page_links = self.find_links(soup)
            self.urls.extend(page_links)
        return self.urls


# Initialize variables
buy = []
base_url = "https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&priceType=SALE_PRICE"
total_pages = 333

# Scrape the links
url_scraper = Urls()
all_links = url_scraper.scrape_multiple_pages(base_url, total_pages)

buy.extend(all_links)

buy_set = set(buy)

print(buy_set)
print(len(buy_set))