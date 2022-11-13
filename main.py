import yaml
import json
import sys
import logging
import helpers
import time as t


# importing scraper configuration
CONFIG = yaml.safe_load(open("./config.yaml"))
START_YEAR = CONFIG["scraper_start_year"]
END_YEAR = CONFIG["scraper_end_year"]
START_ISSUE = CONFIG["scraper_start_issue"]
END_ISSUE = CONFIG["scraper_end_issue"]
WAIT = CONFIG["scraper_wait"]
CSV = CONFIG["scraper_save_article_links_to_csv"]
CSV_PATH = CONFIG["scraper_csv_path"]
LOG_LEVEL = CONFIG["scraper_log"]
DIALOG = CONFIG["scraper_dialog"]

if LOG_LEVEL:
    logging.basicConfig(level=logging.INFO)

if DIALOG:
    conf_inf = f"The scraper will run from {START_ISSUE}/{START_YEAR} to {END_ISSUE}/{END_YEAR}. Wait time between requests is {WAIT} seconds. Save to csv file is set to {CSV}. Start the scraper? (y/n)"
    conf_check = input(conf_inf)
    if conf_check.lower() == "n":
        sys.exit()

article_links = helpers.get_article_links(
    START_YEAR, END_YEAR, START_ISSUE, END_ISSUE, WAIT
)

if CSV:
    helpers.save_article_links_to_csv(article_links, path=CSV_PATH)

logging.info(f"Successfully scraped {len(article_links)} article links.")

article_id = 1
articles_dict = {}
for article_link in article_links:
    temp = helpers.Article(article_link)
    articles_dict[article_id] = temp.to_dict()
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(articles_dict, f, indent=4, ensure_ascii=False)
    logging.info(
        f"Successfully scraped {article_id} of {len(article_links)} articles. ETA {(len(article_links) - article_id) * 5} seconds."
    )
    article_id += 1
    t.sleep(WAIT)
