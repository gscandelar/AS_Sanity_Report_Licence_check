import csv
import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

INPUT_FILE = "input/article_list.csv"
OUTPUT_FILE = "output/results.csv"
BASE_URL = "https://wpp-admin-wprod.aws.wiley.com/services/wpp-admin-app/productDetails/v1/article/{}"
COOKIES_FILE = "cookies.txt"

MAX_WORKERS = 10  # Number of simultaneous threads (adjust as you need)


def load_cookies(file_path):
    """Loads cookies from a file and returns them as a string"""
    cookies = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                cookies.append(line)
    return "; ".join(cookies)


def read_article_ids(file_path):
    """Reads IDs from CSV and returns them as a list"""
    ids = []
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if row and row[0].strip():
                ids.append(row[0].strip().rstrip(","))
    return ids


def check_license(article_id, headers):
    """Query the API and check if the license is signed"""
    url = BASE_URL.format(article_id)
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        license_info = data.get("license", {}).get("status", {}).get("id")
        return article_id, "SIGNED" if license_info == "SIGNED" else "NOT SIGNED"

    except Exception as e:
        print(f"Error processing {article_id}: {e}")
        return article_id, "ERROR"


def main():
    if not os.path.exists("output"):
        os.makedirs("output")

    # Load cookies
    cookie_header = load_cookies(COOKIES_FILE)
    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Cookie": cookie_header
    }

    # Read IDs
    article_ids = read_article_ids(INPUT_FILE)

    results = []

    # Process in parallel with ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_id = {executor.submit(check_license, aid, headers): aid for aid in article_ids}

        for future in as_completed(future_to_id):
            article_id, status = future.result()
            print(f"{article_id} -> {status}")
            results.append((article_id, status))

    # Save results to CSV
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ArticleID", "LicenseStatus"])
        writer.writerows(results)


if __name__ == "__main__":
    main()
