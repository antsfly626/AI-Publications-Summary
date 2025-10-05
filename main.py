# import libraries
import pandas as pd

# load data
df = pd.read_csv('SB_publication_PMC.csv')
print(df.info)
print(df.head)  # first 5 rows printed
print("feature list:" + df.columns)  # feature list

# semantic search


# web scraping
import requests
from bs4 import BeautifulSoup
from typing import Dict, Any

SECTION_DELIMITER = "---SECTION_DELIMITER---"


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
    article_body = soup.find(id="article-body") or soup.find("div", class_="article") or soup.find('body')

    elements = article_body.find_all(["p", "h1", "h2", "h3", "h4"])
    full_text_parts = []

    for e in elements:
        text = e.get_text(separator=' ', strip=True)
        if not text:
            continue

        if e.name in ["h1", "h2", "h3", "h4"]:
            full_text_parts.append(f"\n{SECTION_DELIMITER}{text}\n")
        elif e.name == "p":
            full_text_parts.append(text)

    return "\n".join(full_text_parts).strip()


def extract_sections(text):
    if not text:
        return {}

    sections_raw = text.split(SECTION_DELIMITER)

    sections = {}

    for section_block in sections_raw[1:]:

        title_end_index = section_block.find('\n')

        if title_end_index != -1:
            title = section_block[:title_end_index].strip()
            content = section_block[title_end_index:].strip()
        else:
            continue

        if title and content:
            sections[title] = content

    return sections


# ----- ADDED CODE to initialize new columns and save data -----
# Line 98: Initialize a new 'Abstract' column with empty strings
df['Abstract'] = ''

# Loop through each row in the DataFrame
for index, row in df.iterrows():
    url = row['Link']
    print(f"Scraping from URL: {url}")
    try:
        raw_text = get_publication_text(url)

        if raw_text:
            section_dict = extract_sections(raw_text)
            
            abstract_text = section_dict.get('Abstract', '')
            
            df.loc[index, 'Abstract'] = abstract_text

            print(f"Successfully scraped Abstract for {row['Title']}.")

    except requests.exceptions.RequestException as e:
        print(f"Error scraping {url}: {e}")

df.to_csv('SB_publication_PMC_with_abstracts.csv', index=False)
print("Scraping complete. Data saved to 'SB_publication_PMC_with_abstracts.csv'")


df = pd.read_csv('SB_publication_PMC_with_abstracts.csv')
df.to_json('SB_publication_PMC_with_abstracts.json', orient='records', indent=4)
