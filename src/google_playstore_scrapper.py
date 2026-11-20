from google_play_scraper import Sort, reviews
import time
import ast
import os
from typing import Dict, Union

def sanitize_content(content: Union[str, None]) -> str:
    if not content:
        return ""
    return content.replace('"', '').replace('\n', ' ').replace('\r', ' ')

def scrape_app_reviews_to_txt(app_id: str, app_name: str, output_txt_filename: str,
                              lang: str = 'en', country: str = 'us',
                              batch_size: int = 200, max_retries: int = 3) -> None:
    """
    Scrapes all reviews for a given app in batches and writes them to a file.
    """
    try:
        start_time = time.time()
        count = 0
        next_token = None
        retries = 0

        app_name_sanitized = sanitize_content(app_name)

        with open(output_txt_filename, 'a', encoding='utf-8') as txt_file:
            while True:
                try:
                    batch_reviews, next_token = reviews(
                        app_id,
                        lang=lang,
                        country=country,
                        sort=Sort.NEWEST,
                        count=batch_size,
                        continuation_token=next_token
                    )
                except Exception as e:
                    if retries < max_retries:
                        retries += 1
                        print(f"Retry {retries}/{max_retries} for {app_name} due to error: {e}")
                        time.sleep(2)
                        continue
                    else:
                        print(f"Failed after {max_retries} retries for {app_name}: {e}")
                        break

                if not batch_reviews:
                    break

                for review in batch_reviews:
                    count += 1
                    content = sanitize_content(review.get('content'))
                    score = review.get('score', 0)
                    txt_file.write(f"{count}, \"{app_name_sanitized}\", \"{content}\", {score}\n")

                if not next_token:
                    break

        elapsed_time = time.time() - start_time
        print(f"Scraped {count} reviews for {app_name} in {elapsed_time:.2f} seconds")

    except Exception as e:
        print(f"Failed to scrape reviews for {app_name}: {e}")


def process_input_mode(data_path: str, output_path: str, mode: str) -> None:
    if mode == "english":
        with open(data_path, 'r', encoding='utf-8') as file:
            apps_dict: Dict[str, str] = ast.literal_eval(file.read())
            for app_id, app_name in apps_dict.items():
                print(f"Now scraping: {app_name} ({app_id})")
                scrape_app_reviews_to_txt(app_id, app_name, output_path)
    else:
        with open(data_path, 'r', encoding='utf-8') as file:
            for line in file:
                app_id, app_name, lang, country = line.strip().split(', ')

                app_id = app_id.strip("'")
                app_name = app_name.strip("'")
                lang = lang.strip("'")
                country = country.strip("'")

                print(f"Now scraping: {app_name} ({app_id}) [lang={lang}, country={country}]")

                scrape_app_reviews_to_txt(
                    app_id,
                    app_name,
                    output_path,
                    lang,
                    country
                )




def main() -> None:
    mode = "non_english"
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
    base_path = os.path.join(data_dir, '0_app_lists', '2026')
    save_path = os.path.join(data_dir, '1_raw', '2026')
    data_filename = 'google_playstore_list_new.txt' if mode == "english" else 'google_playstore_list_new_additional.txt'
    output_filename = 'google_app_reviews.csv' if mode == "english" else 'google_playstore_list_additional.csv'

    data_path = os.path.join(base_path, data_filename)
    output_path = os.path.join(save_path, output_filename)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write("id, app, content, score\n")

    process_input_mode(data_path, output_path, mode)


if __name__ == "__main__":
    main()
