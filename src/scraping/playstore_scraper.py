from google_play_scraper import reviews, Sort
import csv
from datetime import datetime
import logging
from pathlib import Path
import time

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
log_dir = project_root / 'logs'
data_dir = project_root / 'data' / 'raw'

log_dir.mkdir(parents=True, exist_ok=True)
data_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / 'scraper.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

BANK_APPS = {
    'Commercial Bank of Ethiopia': 'com.combanketh.mobilebanking',
    'Bank of Abyssinia': 'com.boa.boaMobileBanking',
    'Dashen Bank': 'com.cr2.amolelight'
}

def scrape_bank_reviews(app_id: str, bank_name: str, count: int = 500, retries: int = 3):
    for attempt in range(retries):
        try:
            logging.info(f"🔄 Scraping {count} reviews for {bank_name}...")
            result, _ = reviews(
                app_id,
                lang='en',
                country='et',
                sort=Sort.NEWEST,
                count=count
            )
            return result
        except Exception as e:
            logging.error(f"❌ Attempt {attempt + 1}: Failed to scrape {bank_name}: {str(e)}")
            if attempt < retries - 1:
                wait_time = 2 ** attempt
                logging.info(f"⏳ Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                logging.error(f"❌ All attempts to scrape {bank_name} failed.")
                return []

def format_review(review: dict, bank_name: str) -> dict:
    return {
        'Review Text': review['content'],
        'Rating': review['score'],
        'Date': review['at'].strftime('%Y-%m-%d'),
        'Bank/App Name': bank_name,
        'Source': 'Google Play'
    }

def save_to_csv(data: list, filename: str) -> bool:
    try:
        with open(data_dir / filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        return True
    except Exception as e:
        logging.error(f"❌ Failed to save CSV: {str(e)}")
        return False

def main():
    all_reviews = []

    for bank_name, app_id in BANK_APPS.items():
        bank_reviews = scrape_bank_reviews(app_id, bank_name)
        if bank_reviews:
            formatted = [format_review(r, bank_name) for r in bank_reviews]
            all_reviews.extend(formatted)
            logging.info(f"✅ Collected {len(formatted)} reviews for {bank_name}")

    total = len(all_reviews)
    if total < 1200:
        logging.warning(f"⚠️ Only collected {total} reviews (minimum 1200 required)")
    else:
        logging.info(f"🎉 Successfully collected {total} reviews")

    if all_reviews:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        if save_to_csv(all_reviews, f'all_reviews_{timestamp}.csv'):
            logging.info(f"💾 Saved all reviews to {data_dir}/all_reviews_{timestamp}.csv")

        print(f"\nTotal reviews collected: {total}")
        if total >= 1200:
            print("Criteria met.")
        else:
            print("Minimum of 1200 reviews not met.")

        print("\nSample data:")
        for review in all_reviews[:5]:
            print(review)

if __name__ == '__main__':
    logging.info("=== Starting Play Store Scraper ===")
    main()
    logging.info("=== Scraping Completed ===")