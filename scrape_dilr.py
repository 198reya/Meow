import os
import re
import requests
import csv
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# ——— CONFIG ———
YEARS      = ["2022", "2023", "2024"]
SECTION    = "DI-LR"
SLOTS      = [1, 2, 3]
BASE_TMPL  = "https://online.2iim.com/CAT-question-paper/CAT-{year}-Question-Paper-Slot-{slot}-DILR/"
OUTPUT_CSV = "dilr_master.csv"
IMG_DIR    = "images"
HEADERS    = {"User-Agent": "Mozilla/5.0"}

os.makedirs(IMG_DIR, exist_ok=True)

# ——— UTIL: download images & return local paths ———
def download_images(img_tags, prefix):
    paths = []
    for i, img in enumerate(img_tags, start=1):
        src = img.get("src") or img.get("data-src")
        if not src:
            continue
        full_url = urljoin(base_url, src)
        ext = os.path.splitext(src.split("?")[0])[1] or ".jpg"
        fname = f"{prefix}_{i}{ext}"
        fpath = os.path.join(IMG_DIR, fname)
        if not os.path.exists(fpath):
            r = requests.get(full_url, headers=HEADERS)
            r.raise_for_status()
            with open(fpath, "wb") as f:
                f.write(r.content)
        paths.append(fpath)
    return paths

# ——— MAIN LOOP ———
fieldnames = [
    "Year","Section","Slot",
    "ScenarioText","ImageFiles",
    "QuestionText","AnswerType","Options","CorrectAnswer"
]
all_rows = []

for year in YEARS:
    for slot in SLOTS:
        base_url = BASE_TMPL.format(year=year, slot=slot)
        try:
            resp = requests.get(base_url, headers=HEADERS)
            resp.raise_for_status()
        except Exception as e:
            print(f"Error accessing {year} Slot {slot}: {e}")
            continue

        soup = BeautifulSoup(resp.text, "html.parser")

        ol = soup.select_one("ol.ques")
        if not ol:
            print(f"No DI‑LR block found for {year} Slot {slot}, skipping.")
            continue

        scenario_counter = 0
        current_scenario = ""
        current_images   = []

        for child in ol.children:
            if getattr(child, "name", None) == "p" and child.get("align") == "justify":
                scenario_counter += 1
                current_scenario = child.get_text(" ", strip=True)
                imgs = child.find_all("img")
                prefix = f"{year}_slot{slot}_scen{scenario_counter}"
                current_images = download_images(imgs, prefix)
                print(f"[{year} • Slot {slot} • Scenario {scenario_counter}] downloaded {len(current_images)} image(s)")

            elif getattr(child, "name", None) == "li":
                p = child.find("p")
                qtext = p.get_text(" ", strip=True) if p else ""

                opts = [o.get_text(strip=True) for o in child.select("ol.choice li")]
                atype = "MCQ" if opts else "Numerical"
                opts_str = " | ".join(opts)

                span = child.find("span", class_="tooltiptext")
                raw = span.get_text(strip=True) if span else ""
                if atype == "MCQ":
                    m = re.search(r"Choice\s*([A-D])", raw)
                    correct = m.group(1) if m else raw
                else:
                    correct = raw

                all_rows.append({
                    "Year": year,
                    "Section": SECTION,
                    "Slot": slot,
                    "ScenarioText": current_scenario,
                    "ImageFiles": " | ".join(current_images),
                    "QuestionText": qtext,
                    "AnswerType": atype,
                    "Options": opts_str,
                    "CorrectAnswer": correct
                })

        print(f"→ Completed {year} Slot {slot}, total questions so far: {len(all_rows)}")

# ——— WRITE CSV ———
with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_rows)

print(f"\nScraped a total of {len(all_rows)} questions from all slots and years.")
print(f"→ Data written to {OUTPUT_CSV}")
print(f"→ Images stored in ./{IMG_DIR}/")
