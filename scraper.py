from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import requests
import json

class Scraper:
    def __init__(self, ticker):
        self.ticker = ticker
        self.url = f"https://www.screener.in/company/{ticker}/consolidated/"
        self.soup = self.get_soup()
        
    def get_soup(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")

        driver = webdriver.Chrome(options=options)
        driver.get(self.url)

        # Let the page load
        time.sleep(2)

        # Click all dropdown buttons with class 'button-plain'
        buttons = driver.find_elements(By.CLASS_NAME, "button-plain")
        for button in buttons:
            try:
                driver.execute_script("arguments[0].click();", button)
                time.sleep(0.2)  # Give time for dynamic content to load
            except Exception as e:
                print(f"Could not click a button: {e}")

        # Get final page source after all dropdowns are expanded
        html = driver.page_source
        driver.quit()

        return BeautifulSoup(html, 'html.parser')
        
    def get_company_info(self):
        company_info = {}
        info = self.soup.find('ul', id='top-ratios')

        for li in info.find_all('li'):
            name = li.find('span', class_ = "name").text.strip()
            numbers = [n.text.strip() for n in li.find_all('span', class_ = "number")]
            val = "/".join(numbers) if numbers else "N/A"
            company_info[name] = val
            
        return(company_info)
    
    def get_balance_sheet(self):
        balance_sheet = {}
        balance_sheet_sec = self.soup.find('section', id='balance-sheet')
        balance_sheet_table = balance_sheet_sec.find('tbody')
        for row in balance_sheet_table.find_all('tr'):
            tds = row.find_all('td')
            if not tds:
                return None
            row_name = tds[0].text.strip()
            values = [td.text.strip().replace(",", "") for td in tds[1:]]  # remove commas for numbers
            
            row_data =  {row_name: values}
            balance_sheet.update(row_data)
        return balance_sheet
    
x = Scraper('ADANIENT').get_balance_sheet()
print(json.dumps(x, indent=4))