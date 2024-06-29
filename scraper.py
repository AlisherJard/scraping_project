from bs4 import BeautifulSoup
import requests
import re
import json
import pandas as pd

class Classified():
    """
    Representation of a proprety, based on a immoweb url
    """

    def __init__(self,house_url : str) -> None:
        self.locality = None
        self.type = None
        self.subtype = None
        self.price = None
        self.sale_type = None
        self.rooms = None
        self.living_area = None
        self.equipped_kitchen = None
        self.furnished = None
        self.fire = None
        self.terrace = None
        self.terrace_area = None
        self.garden = None
        self.garden_area = None
        self.plot_surface = None
        self.facades = None
        self.pool = None
        self.state = None
        self.infos = self.get_dict(house_url)
        self._set_infos(True)

    def get_dict(self,url:str) -> dict:
        """
        Scrape one page and return the results as a dict

        :param str url: Complete url of the page
        """
        
        text = requests.get(f"{url}",headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
        soup = BeautifulSoup(text.text,features="html.parser")
        
        for tag in soup.find_all(type="text/javascript"):
            if "window.classified" in str(tag.string):
                ndict = tag.string.strip()
                ndict = re.findall(r"\{.*\}", str(ndict))
                return json.loads(ndict[0])

    def _type(self,c_type : str) -> int:
        '''Sets the type to a numerical value
        HOUSE = 1
        APARTMENT = 2'''
        type_list = ["HOUSE","APARTMENT"]
        if c_type in type_list:
            return type_list.index(c_type)+1
        
    def _sale_type(self,sale_type : str) -> int:
        '''Sets the sale_type to a numerical value
        FOR_SALE = 1
        FOR_RENT = 2'''
        type_list = ["FOR_SALE","FOR_RENT"]
        if sale_type in type_list:
            return type_list.index(sale_type)+1
        
    def _kitchen(self,kitchen_type : str) -> int:
        '''Evaluate if the kitchen is fully equipped or not'''
        if kitchen_type == "HYPER_EQUIPPED":
            return 1
        else:
            return 0
        
    def _bool_num(self,value : str) -> int:
        """Transform boolean value into numerical one"""
        if value == True:
            return 1
        elif value == False:
            return 0

    def _set_infos(self, fprint:bool = False) -> None:
        if fprint == True:
            j = json.dumps(self.infos, indent=4)
            with open("house.json", "w") as file:
                print(j, file=file)
        if self.infos == None:
            return
        self.locality = self.infos["property"]["location"]["postalCode"] if "property" in self.infos else None
        self.type = self._type(self.infos["property"]["type"])
        self.subtype = self.infos["property"]["subtype"]
        self.price = self.infos["price"]["mainValue"]
        self.sale_type = self._sale_type(self.infos["transaction"]["type"])
        self.rooms = (self.infos["property"]["bedroomCount"])
        self.living_area = int(self.infos["property"]["netHabitableSurface"]) if self.infos["property"]["netHabitableSurface"] != None else None
        self.equipped_kitchen = self._kitchen(self.infos["property"]["kitchen"]["type"]) if self.infos["property"]["kitchen"] != None else None
        self.furnished = self._bool_num(self.infos["transaction"]["sale"]["isFurnished"]) if self.sale_type == 1 else self._bool_num(self.infos["transaction"]["rental"]["isFurnished"])
        self.fire = self._bool_num(self.infos["property"]["fireplaceExists"])
        self.terrace = self._bool_num(self.infos["property"]["hasTerrace"])
        self.terrace_area = self.infos["property"]["terraceSurface"]
        self.garden = self._bool_num(self.infos["property"]["hasGarden"])
        self.garden_area = self.infos["property"]["gardenSurface"]
        self.plot_surface = self.infos["property"]["land"]["surface"] if self.infos["property"]["land"] != None else None
        self.facades = self.infos["property"]["building"]["facadeCount"] if self.infos["property"]["building"] != None else None
        self.pool = self._bool_num(self.infos["property"]["hasSwimmingPool"])
        self.state = self.infos["property"]["building"]["condition"] if self.infos["property"]["building"] != None else None
    
    def to_df(self,df : pd.DataFrame):
        """Translate attributes of the object into a pandas dataframe"""
        series = vars(self)
        series.pop("infos")
        if len(df.index) == 0:
            df = pd.DataFrame([series])
        else:
            df.loc[len(df.index)] = series
        return df