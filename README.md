Parsing_Zastavok.net is a Python script for scraping wallpapers from Zastavok.net. The script efficiently retrieves high-quality images from specified categories or pages on the website and saves them locally.

[![Run Unit Tests](https://github.com/andblizz/parsing_zastavok.net/actions/workflows/test.yml/badge.svg?event=push)](https://github.com/andblizz/parsing_zastavok.net/actions/workflows/test.yml)

Usage

The scraper can be run directly using the main.py script. Below is an example of how to execute it:

Command-line Options:

	•	--start-page: (Required) The starting page number for scraping.
	•	--end-page: (Required) The ending page number for scraping.
	•	--output-dir: (Optional) The directory to save downloaded images. Defaults to pics/.

Example Command:

Run the scraper to download images from pages 1 to 5 and save them in the output_images directory:
```bash
python main.py --start-page 1 --end-page 2 --output-dir output_images
```
If you want to use the default output directory (pics/), omit the --output-dir argument.
