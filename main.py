import yaml
import sys
import helpers
import time as t

# importing scraper configuration
CONFIG = yaml.safe_load(open("./config.yml"))
START_YEAR = CONFIG["scraper_start_year"]
END_YEAR = CONFIG["scraper_end_year"]
START_ISSUE = CONFIG["scraper_start_issue"]
END_ISSUE = CONFIG["scraper_end_issue"]
WAIT = CONFIG["scraper_wait"]

conf_inf = f"The scraper will run from {START_ISSUE}/{START_YEAR} to {END_ISSUE}/{END_YEAR}. Wait time between requests is {WAIT} seconds. Start the scraper? (y/n)"
conf_check = input(conf_inf)
if conf_check.lower() == "n":
    sys.exit()


for article in helpers.get_article_links(
    START_YEAR, END_YEAR, START_ISSUE, END_ISSUE, WAIT
):
    temp = helpers.Article(article)
    t.sleep(WAIT)
    print(temp)
