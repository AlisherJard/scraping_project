from scraper import Classified
from class_urls import Urls
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd

url_scraper = Urls()

def scrape_website(total_pages:int = 333):
    base_url = "https://www.immoweb.be/en/search/house-and-apartment/"
    combined_url = ["for-sale?countries=BE","for-rent?countries=BE"]
    df = pd.DataFrame()
    link_set = get_links(base_url,combined_url,total_pages)

    with ThreadPoolExecutor(max_workers=40) as executor:
        futures = [executor.submit(get_page, link, df) for link in link_set]
        for futures in as_completed(futures):
            house = futures.result()
            df = house.to_df(df)
    return df

def get_links(base_url:str, combined_url:list[str], total_pages:int = 333):
    link_set = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(url_scraper.scrape_multiple_pages, base_url+url_type, total_pages) for url_type in combined_url]
        for futures in as_completed(futures):
            links = futures.result()
            link_set.extend(links)
    return set(link_set)

def get_page(link:str, df:pd.DataFrame):
    print(f"Scraping page {link}")
    house = Classified(link)
    return house

df = scrape_website()
print(len(df))
df.to_csv("dataset.csv",na_rep=None)