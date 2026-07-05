import sqlite3
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import os

# Optional: LLM integration (Grok, OpenAI, etc.)
# pip install openai  # or groq, etc.
from openai import OpenAI  # placeholder - replace with your preferred LLM

DB_PATH = "device_database.db"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; DeviceDB-Bot/1.0)"}

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def scrape_gsmarena(brand, model_name):
    """Improved GSMArena scraper"""
    query = f"{brand} {model_name}".replace(" ", "+")
    search_url = f"https://www.gsmarena.com/results.php3?sFreeText={query}"
    try:
        resp = requests.get(search_url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        result_link = soup.select_one('a[href*=".php"]')  # first phone link
        if not result_link:
            return None
        detail_url = "https://www.gsmarena.com/" + result_link['href']
        
        detail_resp = requests.get(detail_url, headers=HEADERS, timeout=15)
        detail_soup = BeautifulSoup(detail_resp.text, 'html.parser')
        
        # Extract key specs (expand as needed)
        specs = {}
        for section in ['Network', 'Launch', 'Body', 'Display', 'Platform', 'Memory', 'Camera', 'Battery']:
            th = detail_soup.find('th', string=lambda t: t and section in t)
            if th:
                td = th.find_next('td')
                if td:
                    specs[section.lower()] = td.get_text(strip=True)
        
        return {
            "specs": specs,
            "gsmarena_url": detail_url,
            "scraped_at": datetime.now().isoformat()
        }
    except Exception as e:
        print(f"Scraping failed for {brand} {model_name}: {e}")
        return None

def llm_enrich(data, brand, model_name):
    """Use LLM to generate red flags, repair info, API usage, etc."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # or Grok / other
    
    prompt = f"""You are a device repair and tech expert.
    Device: {brand} {model_name}
    Available data: {json.dumps(data, indent=2)}
    
    Generate comprehensive JSON with:
    - red_flags_warnings (list of issues)
    - repair_youtube_links (example links or search terms)
    - api_usage (public APIs, developer docs if any)
    - known_issues, unlock_root_methods, community_resources, etc.
    - Overall repairability assessment.
    
    Return valid JSON only."""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # or grok, claude, etc.
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        enriched = json.loads(response.choices[0].message.content)
        return enriched
    except Exception as e:
        print(f"LLM enrichment failed: {e}")
        return {}

def populate_missing():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, brand, model_name, specs 
        FROM devices 
        WHERE specs IS NULL OR red_flags_warnings IS NULL 
        LIMIT 10
    """)
    rows = cursor.fetchall()
    
    for row in rows:
        print(f"Processing {row['brand']} {row['model_name']}")
        
        scraped = scrape_gsmarena(row['brand'], row['model_name'])
        if scraped:
            enriched = llm_enrich(scraped, row['brand'], row['model_name'])
            
            update_data = {
                "specs": json.dumps(scraped["specs"]),
                "sources": json.dumps([scraped.get("gsmarena_url")]),
                **{k: json.dumps(v) if isinstance(v, dict) else v for k, v in enriched.items()}
            }
            
            set_clause = ", ".join([f"{k} = ?" for k in update_data.keys()])
            cursor.execute(f"UPDATE devices SET {set_clause}, last_updated = CURRENT_TIMESTAMP WHERE id = ?",
                          list(update_data.values()) + [row['id']])
            conn.commit()
            print("✓ Updated")
        
        time.sleep(5)  # Rate limit friendly
    
    conn.close()

if __name__ == "__main__":
    populate_missing()
