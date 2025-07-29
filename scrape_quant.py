import requests
from bs4 import BeautifulSoup
import csv
import re
import time


SLOT_URL_TEMPLATE = "https://online.2iim.com/CAT-question-paper/CAT-{}-Question-Paper-Slot-{}-Quant/"
YEARS = [2022, 2023, 2024]
SLOTS = [1, 2, 3]
OUTPUT_CSV = "quant_master.csv"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}


fieldnames = [
    "Year", "Section", "Slot", "Topic",
    "Question", "AnswerType",
    "Options", "CorrectAnswer"
]

all_rows = []


for year in YEARS:
    print(f"\nScraping CAT {year}...")
    
    for slot in SLOTS:
        url = SLOT_URL_TEMPLATE.format(year, slot)
        print(f"  Scraping Slot {slot}...", end=" ")
        
        try:
            resp = requests.get(url, headers=HEADERS, timeout=10)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            
            slot_questions = 0
            
           
            for li in soup.select("ol.ques > li"):
              
                h4 = li.find("h4")
                h4_text = h4.get_text(strip=True) if h4 else ""
                parts = [p.strip() for p in h4_text.split(" - ")]
           
                year_extracted = ""
                m_year = re.search(r"CAT\s+(\d{4})", parts[0]) if parts else None
                if m_year:
                    year_extracted = m_year.group(1)
                else:
                    year_extracted = str(year)  
                
                section = parts[1] if len(parts) > 1 else ""
                topic = parts[2] if len(parts) > 2 else ""
                
            
                q_tag = li.find("p")
                question = q_tag.get_text(strip=True) if q_tag else ""
                
              
                if not question:
                    continue
                
               
                opts = [o.get_text(strip=True) for o in li.select("ol.choice li")]
                answer_type = "MCQ" if opts else "Numerical"
                opts_str = " | ".join(opts)
                
             
                span = li.find("span", class_="tooltiptext")
                raw_ans = span.get_text(strip=True) if span else ""
                
                if answer_type == "MCQ":
                    m = re.search(r"Choice\s*([A-D])", raw_ans)
                    correct = m.group(1) if m else raw_ans
                else:
                   
                    lines = raw_ans.split('\n')
                    correct = ""
                    for line in lines:
                        line = line.strip()
                        if line and not line.startswith('Correct:') and not line.startswith('Incorrect:') and not line.startswith('Unattempted:'):
                           
                            if re.search(r'\d', line) and not line.startswith('Choice'):
                                correct = line
                                break
                    if not correct:
                        correct = raw_ans
                
                all_rows.append({
                    "Year": year_extracted,
                    "Section": section,
                    "Slot": slot,
                    "Topic": topic,
                    "Question": question,
                    "AnswerType": answer_type,
                    "Options": opts_str,
                    "CorrectAnswer": correct
                })
                
                slot_questions += 1
            
            print(f"scraped {slot_questions} questions ✓")
            
        except Exception as e:
            print(f"Failed: {e}")
        
       
        time.sleep(1.5)

print(f"\nWriting data to {OUTPUT_CSV}...")
with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_rows)

print(f"\n Total questions scraped: {len(all_rows)}")
print(f" Saved to {OUTPUT_CSV}")


print(f"\nSummary by Year:")
for year in YEARS:
    year_data = [row for row in all_rows if row['Year'] == str(year)]
    mcq_count = len([row for row in year_data if row['AnswerType'] == 'MCQ'])
    numerical_count = len([row for row in year_data if row['AnswerType'] == 'Numerical'])
    print(f"  {year}: {len(year_data)} questions ({mcq_count} MCQ, {numerical_count} Numerical)")

print(f"\nSummary by Slot (all years):")
for slot in SLOTS:
    slot_data = [row for row in all_rows if row['Slot'] == slot]
    print(f"  Slot {slot}: {len(slot_data)} questions")

print(f"\nOverall:")
mcq_total = len([row for row in all_rows if row['AnswerType'] == 'MCQ'])
numerical_total = len([row for row in all_rows if row['AnswerType'] == 'Numerical'])
print(f"  MCQ: {mcq_total}")
print(f"  Numerical: {numerical_total}")
print(f"  Total: {len(all_rows)}")


print(f"\nMost Common Topics (2024):")
topics_2024 = {}
for row in all_rows:
    if row['Year'] == '2024' and row['Topic']:
        topic = row['Topic']
        topics_2024[topic] = topics_2024.get(topic, 0) + 1

sorted_topics = sorted(topics_2024.items(), key=lambda x: x[1], reverse=True)
for topic, count in sorted_topics[:10]:
    print(f"  {topic}: {count} questions")