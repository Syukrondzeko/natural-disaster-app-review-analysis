import csv
import time
from pathlib import Path
from app_store_web_scraper import AppStoreEntry

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
INPUT_FILE = DATA_DIR / "0_app_lists" / "2026" / "apple_app_store_list_new.txt"
OUTPUT_FILE = DATA_DIR / "1_raw" / "2026" / "apple_app_reviews.csv"


def sanitize_content(text):
    if not text:
        return ""
    return text.replace("\n", " ").replace("\r", " ").strip()


def read_app_list(path):
    apps = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = [p.strip().strip("'").strip('"') for p in line.split(",")]
            app_id, app_name, country = parts

            app_id = app_id.replace("id", "").strip()
            apps.append((app_id, app_name, country))

    return apps


def main():
    apps = read_app_list(INPUT_FILE)

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["id", "app", "content", "score"])

        for app_id, app_name, country in apps:
            print(f"Scraping: {app_name} ({country})")

            try:
                entry = AppStoreEntry(
                    app_id=app_id,
                    country=country
                )

                count = 0
                for r in entry.reviews():
                    writer.writerow([
                        app_id,
                        app_name,
                        sanitize_content(r.review),
                        r.rating
                    ])
                    count += 1

                print(f"Collected {count} reviews")

            except Exception as e:
                print(f"Failed: {app_name} -> {e}")

            time.sleep(2)  # rate limit

    print("Done. CSV saved.")


if __name__ == "__main__":
    main()
