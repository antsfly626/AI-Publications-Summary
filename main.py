# import libraries
import pandas as pd
import requests
from bs4 import BeautifulSoup
from typing import Dict, Any
import json

# load data
df = pd.read_csv('SB_publication_PMC.csv')
print(df.info())
print(df.head())
print("feature list:", df.columns.tolist())

# --- Web scraping functions ---
SECTION_DELIMITER = "---SECTION_DELIMITER---"

def get_publication_content(url: str) -> Dict[str, Any]:
    """
    Scrapes a publication URL for text, images, and tables.
    Returns a dictionary with the extracted content.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/117.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Referer": "https://www.google.com/"
    }

    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        article_body = soup.find(id="article-body") or soup.find("div", class_="article") or soup.find('body')

        # --- Extract text sections ---
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
        full_text = "\n".join(full_text_parts).strip()

        # --- Extract images ---
        images = []
        img_tags = article_body.find_all("img")
        for img in img_tags:
            src = img.get("src")
            if src:
                if not src.startswith(('http', 'https')):
                    src = requests.compat.urljoin(url, src)
                images.append(src)

        # --- Extract tables (using pandas) ---
        tables = []
        try:
            list_of_dfs = pd.read_html(r.text, flavor='bs4')
            for df_table in list_of_dfs:
                tables.append(df_table.to_json(orient='split'))
        except Exception as e:
            print(f"No tables found or error parsing tables from {url}: {e}")

        return {
            'text': full_text,
            'images': images,
            'tables': tables
        }

    except requests.exceptions.RequestException as e:
        print(f"Error scraping {url}: {e}")
        return None

def extract_sections(text: str) -> Dict[str, str]:
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

# --- Main script ---

# Initialize new columns
df['Abstract'] = ''
df['Images'] = [[] for _ in range(len(df))]
df['Tables'] = [[] for _ in range(len(df))]

# Loop through each row in the DataFrame
for index, row in df.iterrows():
    url = row['Link']
    print(f"Scraping from URL: {url}")
    
    scraped_content = get_publication_content(url)
    
    if scraped_content:
        section_dict = extract_sections(scraped_content['text'])
        
        df.loc[index, 'Abstract'] = section_dict.get('Abstract', '')
        df.loc[index, 'Images'] = json.dumps(scraped_content['images'])
        df.loc[index, 'Tables'] = json.dumps(scraped_content['tables'])
        
        print(f"Successfully scraped content for {row['Title']}.")

# Save data to CSV and JSON
df.to_csv('SB_publication_PMC_with_full_content.csv', index=False)
df.to_json('SB_publication_PMC_with_full_content.json', orient='records', indent=4)

print("Scraping complete. Data saved to 'SB_publication_PMC_with_full_content.csv' and 'SB_publication_PMC_with_full_content.json'")