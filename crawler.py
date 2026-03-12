from vnstock import Vnstock
import pandas as pd
import os
import time

from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

from config import *
from logger import logger


def crawl_symbol(symbol):

    symbol = symbol.strip()

    now = datetime.now()
    date_str = now.strftime("%d%m%Y")
    time_str = now.strftime("%H%M")

    for attempt in range(RETRY):

        try:

            stock = Vnstock().stock(symbol=symbol, source="VCI")

            df = stock.quote.intraday(page_size=PAGE_SIZE)

            raw_dir = os.path.join(DATA_DIR, symbol, "raw", date_str)
            os.makedirs(raw_dir, exist_ok=True)

            filename = f"{symbol}-{date_str}-{time_str}.csv"
            filepath = os.path.join(raw_dir, filename)
            
            df.to_csv(filepath, index=False)

            logger.info(f"{symbol} saved | rows={len(df)}")

            return

        except Exception as e:

            logger.warning(f"{symbol} retry {attempt+1} | {e}")

            time.sleep(RETRY_SLEEP)

    logger.error(f"{symbol} FAILED after retries")


def run_crawler():

    logger.info("Crawler started")

    with open(SYMBOL_FILE) as f:
        symbols = f.read().strip().split(",")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:

        executor.map(crawl_symbol, symbols)

    logger.info("Crawler finished")

if __name__ == "__main__":

    run_crawler()