import csv
import json
import time
import random
import requests

from bs4 import BeautifulSoup
from pathlib import Path


def scrape_assessment(url):
    print(f"Scraping: {url}")

    res = safe_get(url)   # ✅ use safe_get instead of requests.get
    if res is None:
        print(f"Skipping due to repeated failures: {url}")
        return {
            "assessment_name": "",
            "url": url,
            "description": "",
            "job_levels": "",
            "assessment_length": "",
            "test_type": ""
        }
    soup = BeautifulSoup(res.text, "html.parser")

    # -----------------------------------
    # 1. NAME (H1 under .content__container)
    # -----------------------------------
    name_tag = soup.find("div", class_="row content__container typ")
    name = ""
    if name_tag:
        h1 = name_tag.find("h1")
        if h1:
            name = h1.text.strip()

    # -----------------------------------
    # 2. MAIN CONTENT BLOCK
    # (The one with data-course-id)
    # -----------------------------------
    block = soup.find("div", attrs={"data-course-id": True})
    if not block:
        return {
            "assessment_name": name,
            "url": url,
            "description": "",
            "job_levels": "",
            "assessment_length": "",
            "test_type": ""
        }

    # -----------------------------------
    # General structure inside block:
    #   <div class="product-catalogue-training-calendar__row typ">
    #       <h4>Section Name</h4>
    #       <p>Value...</p>
    #   </div>
    # -----------------------------------

    rows = block.find_all("div", class_="product-catalogue-training-calendar__row typ")

    description = ""
    job_levels = ""
    assessment_length = ""
    test_type = ""

    for r in rows:
        h4 = r.find("h4")
        if not h4:
            continue

        title = h4.text.strip().lower()

        p = r.find("p")
        value = p.text.strip() if p else ""

        if "description" in title:
            description = value

        elif "job levels" in title:
            job_levels = value

        elif "assessment length" in title:
            assessment_length = value

    # -----------------------------------
    # 5. TEST TYPE (Inside .d-flex span)
    # -----------------------------------
    d_flex_blocks = block.find_all("div", class_="d-flex")
    for d in d_flex_blocks:
        label = d.find("p")
        if label and "Test Type" in label.text:
            span = d.find("span")
            if span:
                test_type = span.text.strip()

    return {
        "assessment_name": name,
        "url": url,
        "description": description,
        "job_levels": job_levels,
        "assessment_length": assessment_length,
        "test_type": test_type
    }


def scrape_all_assessments(url_file="Data/assessments_urls.json", output_csv="Data/assessments.csv"):
    print("Loading URLs...")
    urls = json.load(open(url_file))

    data = []

    for url in urls:
        try:
            info = scrape_assessment(url)
            data.append(info)
        except Exception as e:
            print(f"Failed to scrape {url}: {e}")

    Path(output_csv).parent.mkdir(parents=True, exist_ok=True)

    # Write CSV
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["assessment_name", "url", "description", "job_levels", "assessment_length", "test_type"]
        )
        writer.writeheader()
        writer.writerows(data)

    print(f"\nSaved {len(data)} assessments → {output_csv}")

def safe_get(url, retries=5):
    for attempt in range(retries):
        try:
            return requests.get(url, timeout=10)
        except Exception as e:
            wait = random.uniform(1.5, 4.0)   # random delay avoids detection
            print(f"Request failed ({attempt+1}/{retries}): {e} — retrying in {wait:.1f}s...")
            time.sleep(wait)
    return None

if __name__ == "__main__":
    scrape_all_assessments()