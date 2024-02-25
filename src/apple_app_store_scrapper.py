import os
import time
import csv
from typing import Generator, Tuple
from app_store_scraper import AppStore

def sanitize_content(content: str) -> str:
    """
    Sanitizes the content by removing new lines, carriage returns, and double quotes.

    Args:
        content (str): The review content to sanitize.

    Returns:
        str: The sanitized content.
    """
    return content.replace('\n', ' ').replace('\r', ' ').replace('"', '')

def scrape_app_store_reviews_to_csv(app_id: str, app_name: str, country: str, output_csv_filename: str) -> None:
    """
    Scrapes reviews for a specific app from the App Store and saves them to a CSV file.

    Args:
        app_id (str): The app's unique identifier on the App Store.
        app_name (str): The name of the app.
        country (str): The country code for the App Store.
        output_csv_filename (str): The file path where the reviews will be saved.
    """
    try:
        start_time = time.time()
        app = AppStore(country=country, app_name=app_id)
        app.review()

        os.makedirs(os.path.dirname(output_csv_filename), exist_ok=True)
        is_file_empty = not os.path.exists(output_csv_filename) or os.stat(output_csv_filename).st_size == 0

        with open(output_csv_filename, mode='a', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
            if is_file_empty:
                csv_writer.writerow(["id", "app", "content", "score"])  # Write header only if file is empty

            for index, review in enumerate(app.reviews, start=1):
                content = sanitize_content(review['review'])
                score = review['rating']
                app_name_sanitized = sanitize_content(app_name)
                csv_writer.writerow([index, app_name_sanitized, content, score])

        elapsed_time = time.time() - start_time
        print(f"{len(app.reviews)} reviews from {app_name} scraped and saved to {output_csv_filename} in {elapsed_time:.2f} seconds")

    except Exception as e:
        print(f"Failed to scrape reviews for {app_name}: {e}")

def read_app_data(file_path: str) -> Generator[Tuple[str, str, str], None, None]:
    """
    Reads app data from a file and yields tuples of app ID, app name, and country.

    Args:
        file_path (str): The path to the file containing the app data.

    Yields:
        Generator[Tuple[str, str, str], None, None]: A generator of tuples containing the app ID, app name, and country.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            app_id, app_name, country = line.strip().split(", ")
            yield app_id.strip("'"), app_name.strip("'"), country.strip("'")

if __name__ == "__main__":
    base_path = '.../dataset/phase 0/'
    save_path = '.../dataset/phase 1/'

    data_filename = 'apple_app_store_list.txt'
    output_filename = 'app_store_reviews.csv'

    data_path = os.path.join(base_path, data_filename)
    output_path = os.path.join(save_path, output_filename)

    # Ensure the output CSV file is initialized properly
    if not os.path.exists(output_path) or os.stat(output_path).st_size == 0:
        with open(output_path, 'w', newline='', encoding='utf-8') as csv_file:
            csv.writer(csv_file, quoting=csv.QUOTE_ALL).writerow(["id", "app", "content", "score"])

    for app_id, app_name, country in read_app_data(data_path):
        scrape_app_store_reviews_to_csv(app_id, app_name, country, output_path)
        time.sleep(30)  # Be respectful to the server by waiting before the next request
