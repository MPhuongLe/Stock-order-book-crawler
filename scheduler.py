import schedule
import time

from crawler import run_crawler
from merge import merge_all
from logger import logger
from config import CRAWL_INTERVAL_MINUTES, MERGE_TIME


def job_crawl():
    logger.info("Scheduled crawl triggered")
    run_crawler()


def job_merge():
    logger.info("Scheduled merge triggered")
    merge_all()


schedule.every(CRAWL_INTERVAL_MINUTES).minutes.do(job_crawl)
schedule.every().day.at(MERGE_TIME).do(job_merge)


logger.info(
    f"Scheduler started | crawl={CRAWL_INTERVAL_MINUTES}min | merge={MERGE_TIME}"
)

# run first crawl immediately
run_crawler()

while True:

    schedule.run_pending()

    time.sleep(5)