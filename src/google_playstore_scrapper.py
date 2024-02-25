from google_play_scraper import Sort, reviews_all
import time
import ast
import os
from typing import Dict, Union

def sanitize_content(content: Union[str, None]) -> str:
    """
    Sanitizes the review content by removing problematic characters.

    Args:
        content (Union[str, None]): The review content to be sanitized.

    Returns:
        str: The sanitized content.
    """
    if not content:
        return ""
    return content.replace('"', '').replace('\n', ' ').replace('\r', ' ')

def scrape_app_reviews_to_txt(app_id: str, app_name: str, output_txt_filename: str, lang: str = 'en', country: str = 'us') -> None:
    """
    Scrapes app reviews from the Google Play Store and saves them to a text file.

    Args:
        app_id (str): The Google Play Store ID of the app.
        app_name (str): The name of the app.
        output_txt_filename (str): The output file path for saving the reviews.
        lang (str, optional): The language for the reviews. Defaults to 'en'.
        country (str, optional): The country for the reviews. Defaults to 'us'.
    """
    try:
        start_time = time.time()
        reviews = reviews_all(app_id, sleep_milliseconds=0, lang=lang, country=country, sort=Sort.NEWEST)
        
        with open(output_txt_filename, 'a', encoding='utf-8') as txt_file:
            for index, review in enumerate(reviews, start=1):
                content = sanitize_content(review.get('content'))
                score = review.get('score', 0)
                app_name_sanitized = sanitize_content(app_name)
                txt_file.write(f"{index}, \"{app_name_sanitized}\", \"{content}\", {score}\n")

        elapsed_time = time.time() - start_time
        print(f"Scraped {len(reviews)} reviews for {app_name} in {elapsed_time:.2f} seconds")

    except Exception as e:
        print(f"Failed to scrape reviews for {app_name}: {e}")

def process_input_mode(data_path: str, output_path: str, mode: str) -> None:
    """
    Processes app review scraping based on the specified input mode.

    Args:
        data_path (str): The path to the input data file.
        output_path (str): The path to the output file for saving the reviews.
        mode (str): The mode of operation ('english' for english app, 'non_english' for non english app).
    """
    if mode == "english":
        with open(data_path, 'r', encoding='utf-8') as file:
            apps_dict: Dict[str, str] = ast.literal_eval(file.read())
            for app_id, app_name in apps_dict.items():
                scrape_app_reviews_to_txt(app_id, app_name, output_path)
    else:
        with open(data_path, 'r', encoding='utf-8') as file:
            for line in file:
                app_id, app_name, lang, country = line.strip().split(', ')
                scrape_app_reviews_to_txt(app_id.strip("'"), app_name.strip("'"), output_path, lang.strip("'"), country.strip("'"))

def main() -> None:
    """
    Main function to orchestrate the scraping of app reviews based on input data.
    """
    mode = "english"  # Change to "non_english" as needed
    base_path = '.../dataset/phase 0/'
    save_path = '.../dataset/phase 1/'
    data_filename = 'google_playstore_list_1.txt' if mode == "english" else 'google_playstore_list_2.txt'
    output_filename = 'google_app_reviews_1.csv' if mode == "english" else 'google_app_reviews_2.csv'

    data_path = os.path.join(base_path, data_filename)
    output_path = os.path.join(save_path, output_filename)

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    # Initialize the output file with headers
    with open(output_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write("id, app, content, score\n")

    # Process the input data based on the selected mode
    process_input_mode(data_path, output_path, mode)

if __name__ == "__main__":
    main()
