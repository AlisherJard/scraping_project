from bs4 import BeautifulSoup
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

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
        # for page_num in range(1, total_pages + 1):
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.scrape_page_links,base_url,page_num) for page_num in range(1, total_pages + 1)]
            for futures in as_completed(futures):
                page_links = futures.result()
                self.urls.extend(page_links)
        return self.urls
    
    def scrape_page_links(self,base_url:str,page_num:int):
        url = f"{base_url}&page={page_num}"
        soup = self.scrape(url)
        page_links = self.find_links(soup)
        print(f'Scraping page {page_num}')
        return page_links
