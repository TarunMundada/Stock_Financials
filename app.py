import streamlit as st
from scraper.financial_scraper import Scraper
import json

company_name = "ADANIENT"

@st.cache_data(ttl=3600)
def get_data(company_name):
    scraper = Scraper(company_name)
    return {
        "company_info": scraper.get_company_info(),
        "balance_sheet": scraper.get_balance_sheet(),
        "cash_flow": scraper.get_cash_flow(),
        "profit_loss": scraper.get_profit_loss()
    }


data = get_data(company_name)

# Save to JSON file
with open(f"{company_name.replace(' ', '_').lower()}_data.json", "w") as json_file:
    json.dump(data, json_file, indent=4)