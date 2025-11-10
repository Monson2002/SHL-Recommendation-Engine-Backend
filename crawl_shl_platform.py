import os
import json
import requests

from pathlib import Path
from bs4 import BeautifulSoup

BASE_URL = "https://www.shl.com/products/product-catalog/"

def get_all_catalog_pages():
    urls = []
    start = 0
    step = 12  # SHL shows 12 items per page
    total_pages = 32  

    output_file="Data/pages.txt"

    for page in range(total_pages):
        start = page * step
        url = f"https://www.shl.com/products/product-catalog/?start={start}&type=1"
        urls.append(url)
        print("Page:", page + 1, "→", url)

    # save to file
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w") as f:
        f.writelines(u + "\n" for u in urls)

    print(f"\nSaved {len(urls)} URLs → {output_file}")

    return urls

def load_or_generate_urls_txt(file_path="Data/pages.txt"):
    if os.path.exists(file_path):
        print(f"Loading URLs from {file_path}...")
        with open(file_path, "r") as f:
            return [line.strip() for line in f.readlines() if line.strip()]

    print("URL file not found → Generating...")
    urls = get_all_catalog_pages()

    with open(file_path, "w") as f:
        f.writelines(u + "\n" for u in urls)

    print(f"Saved {len(urls)} URLs → {file_path}")
    return urls

def crawl_shl_catalog(output_path="Data/assessments_urls.json"):
    all_urls = load_or_generate_urls_txt() 
    url_list = []
    print(all_urls)
    print("\nCrawling SHL catalog...")
    for url in all_urls:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")

        # All assessment blocks are inside product cards
        product_cards = soup.find_all("div", class_="custom__table-responsive")

        tables = []
        for div in product_cards:
            tables.extend(div.find_all("table"))
        print(f"Found {len(tables)} tables")

        tds = tables[0].find_all("td", class_="custom__table-heading__title")
        for td in tds:
            a_tag = td.find("a", href=True)
            if a_tag:
                full_url = "https://www.shl.com" + a_tag["href"]
                url_list.append(full_url)

        print(url_list)
        print(f"Found {len(url_list)} assessments")

    # ✅ remove duplicates 
    url_list = list(dict.fromkeys(url_list))

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(url_list, f, indent=2)

    print(f"\nSaved {len(url_list)} assessment URLs → {output_path}")
    return url_list

if __name__ == "__main__":
    crawl_shl_catalog()
