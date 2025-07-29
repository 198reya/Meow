import os
import re
import requests
import pandas as pd
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# ——— CONFIG ———
YEARS = [2022, 2023, 2024]
SLOTS = [1, 2, 3]
BASE_URL = "https://online.2iim.com/CAT-question-paper/CAT-{year}-Question-Paper-Slot-{slot}-VARC/"
OUTPUT_CSV = "varc_master.csv"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def clean(text):
    """Clean and normalize text"""
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text.replace('\xa0', ' ')).strip()

def extract_correct_answer(question_block):
    """Extract correct answer from tooltip"""
    tooltip = question_block.find("span", class_='tooltiptext')
    if not tooltip:
        return ""
    
    tooltip_text = clean(tooltip.get_text())
    # Handle MCQ format (Choice A/B/C/D)
    mcq_match = re.search(r'Choice\s+([A-D])', tooltip_text)
    if mcq_match:
        return mcq_match.group(1)
    # Handle direct answer text
    return tooltip_text

def scrape_varc_page(url):
    """Scrape a single VARC page"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find the main questions container
        container = soup.find('ol', class_='ques')
        if not container:
            print(f"⚠️ No questions container found at {url}")
            return []
        
        questions_data = []
        current_passage = ""
        
        # Process all direct children of the container
        for child in container.children:
            if not getattr(child, 'name', None):  # Skip non-tag elements
                continue
                
            # Detect and update current passage
            if child.name == 'p' and child.get('align') == 'justify':
                current_passage = clean(child.get_text())
                print(f"📖 Found passage: {current_passage[:50]}...")
                continue
                
            # Process question items
            if child.name == 'li':
                # Extract question text
                question_p = child.find('p')
                question_text = clean(question_p.get_text()) if question_p else ""
                
                # Extract options
                options = []
                options_ol = child.find('ol', class_='choice')
                if options_ol:
                    options = [clean(li.get_text()) for li in options_ol.find_all('li')]
                
                # Determine question type
                answer_type = "MCQ" if options else "Numerical"
                
                # Extract correct answer
                correct_answer = extract_correct_answer(child)
                
                questions_data.append({
                    'passage': current_passage,
                    'question': question_text,
                    'options': " | ".join(options),
                    'answer_type': answer_type,
                    'correct_answer': correct_answer
                })
        
        return questions_data
        
    except Exception as e:
        print(f" Error scraping {url}: {e}")
        return []

def main():
    master_data = []
    
    for year in YEARS:
        for slot in SLOTS:
            url = BASE_URL.format(year=year, slot=slot)
            print(f"\n🌐 Scraping {url}")
            
            questions = scrape_varc_page(url)
            for q in questions:
                master_data.append({
                    'year': year,
                    'slot': slot,
                    'section': 'VARC',
                    **q
                })
            
            time.sleep(1.5)  
    
    # Save to CSV
    df = pd.DataFrame(master_data)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"\n Saved {len(master_data)} questions to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()