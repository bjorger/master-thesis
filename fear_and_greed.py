from dotenv import load_dotenv
load_dotenv()
import os
import requests
from bs4 import BeautifulSoup

fear_and_greed_url = os.environ.get("FEAR_AND_GREED_URL")


def fetchFearAndGreedIndex() -> None:
    resp = requests.get(fear_and_greed_url)
    
    soup = BeautifulSoup(resp.content, 'html.parser')
    status_element = soup.find('div', 'status')
    status_element.text
    
    
fetchFearAndGreedIndex()