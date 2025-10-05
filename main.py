# import libraries
import pandas as pd

# load data
df = pd.read_csv('SB_publication_PMC.csv')
print(df.info) 
print(df.head) # first 5 rows printed
print(df.columns) # feature list

# semantic search


# web scraping
import requests
from bs4 import BeautifulSoup

url = "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4136787/"  # example

def get_publication_text(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/117.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Referer": "https://www.google.com/"
    }

    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    elements = soup.find_all(["p", "h1", "h2", "h3", "h4"])
    text = [e.get_text(strip=True) for e in elements if e.get_text(strip=True)]
    print("\n".join(text))

get_publication_text(url)

# def get_publication(link):

# dashboard