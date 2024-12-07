import argparse
from scraper.scraper import scrape_images
from scraper.settings import DEFAULT_OUTPUT_DIR


def main():
    parser = argparse.ArgumentParser(description="Scrape images from a website.")
    parser.add_argument(
        '--start-page', type=int, required=True, help="Starting page number for scraping."
    )
    parser.add_argument(
        '--end-page', type=int, required=True, help="Ending page number for scraping."
    )
    parser.add_argument(
        '--output-dir', type=str, default=DEFAULT_OUTPUT_DIR,
        help="Directory to save downloaded images (default: 'pics/')."
    )
    args = parser.parse_args()

    try:
        print(f"Scraping images from page {args.start_page} to {args.end_page}...")
        scrape_images(args.start_page, args.end_page, args.output_dir)
        print("Scraping completed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
