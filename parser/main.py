from parse import ProductScraper
import config
from writers import JSONFileWriter


if __name__ == "__main__":
    scraper = ProductScraper()
    data = scraper.scrape_all_products()

    writer = JSONFileWriter(file_name=config.MENU_FILE_NAME)
    writer.write_in_json_file(data)
