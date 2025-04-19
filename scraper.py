from bs4 import BeautifulSoup
import requests



class Scraper:
    def __init__(self, ticker):
        self.ticker = ticker
        self.url = f"https://www.screener.in/company/{ticker}/consolidated/"
        self.soup = self.get_soup()
        
    def get_soup(self):
        response = requests.get(self.url)
        if response.status_code != 200:
            raise Exception(f"Failed to load page: {response.status_code}")
        else:
            return BeautifulSoup(response.content, 'html.parser')
        
    def get_company_info(self):
        company_info = {}
        info = self.soup.find('ul', id='top-ratios')

        for li in info.find_all('li'):
            name = li.find('span', class_ = "name").text.strip()
            numbers = [n.text.strip() for n in li.find_all('span', class_ = "number")]
            val = "/".join(numbers) if numbers else "N/A"
            company_info[name] = val
            
        return(company_info)
    
    
print(Scraper('ADANIENT').get_company_info())