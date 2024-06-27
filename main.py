from scraper import Classified
import pandas as pd

url = ["https://www.immoweb.be/en/classified/apartment/for-sale/lier/2500/20000906","https://www.immoweb.be/en/classified/house/for-sale/nassogne/6950/11485698","https://www.immoweb.be/en/classified/house/for-rent/ottignies-louvain-la-neuve/1340/20001129","https://www.immoweb.be/en/classified/villa/for-sale/kortrijk/8510/20000379"]

test = pd.DataFrame()
for link in url:
    house = Classified(link)
    test = house.to_df(test)
print(test)