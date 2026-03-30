import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

# Robust headers to look like a real browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://www.google.com/"
}

all_movie_data = []
base_url = "https://www.boxofficemojo.com/chart/top_lifetime_gross/"

# Scrape the first 1000 movies (offsets 0, 200, 400, 600, 800)
for offset in range(0, 801, 200): 
    print(f"Scraping offset {offset}...")
    url = f"{base_url}?area=XWW&offset={offset}"
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            print(f"Skipping offset {offset} (Status: {response.status_code})")
            continue

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Using the specific table class found from your selector
        table = soup.find('table', class_='mojo-body-table')
        
        if table:
            rows = table.find_all('tr')[1:]  # Skip the header row
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 3:
                    # Column 1: Title | Column 2: Gross | Column 3: Year
                    title = cols[1].get_text(strip=True)
                    gross_raw = cols[2].get_text(strip=True)
                    
                    # Clean the money string
                    gross_clean = ''.join(filter(str.isdigit, gross_raw))
                    
                    all_movie_data.append({
                        'Title': title,
                        'Worldwide Gross': int(gross_clean) if gross_clean else 0,
                        'Release Year': cols[3].get_text(strip=True) if len(cols) > 3 else "N/A"
                    })
        
        # Wait 2 seconds to be polite \>0</
        time.sleep(2)

    except Exception as e:
        print(f"An error occurred at offset {offset}: {e}")

# Save the data
if all_movie_data:
    df = pd.DataFrame(all_movie_data)
    # Remove any potential duplicates
    df = df.drop_duplicates(subset=['Title'])
    df.to_csv('top_1000_movies_fixed.csv', index=False)
    print(f"\nSuccess! Total movies saved: {len(df)}")
    print("File saved as: top_1000_movies_fixed.csv")
else:
    print("\nError: No data extracted. The site might be blocking the request.")
