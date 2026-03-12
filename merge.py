import os
import pandas as pd

from config import DATA_DIR
from logger import logger


def merge_symbol(symbol):

    folder = os.path.join(DATA_DIR, symbol)

    if not os.path.exists(folder):
        return

    files = [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.endswith(".csv")
    ]

    if not files:
        return

    dfs = []

    for f in files:
        try:
            dfs.append(pd.read_csv(f))
        except Exception as e:
            logger.error(f"{f} read error | {e}")

    df = pd.concat(dfs, ignore_index=True)

    before = len(df)

    # drop duplicate rows
    df = df.drop_duplicates()

    after = len(df)

    logger.info(f"{symbol} duplicates removed: {before-after}")

    output = os.path.join(folder, f"{symbol}_FULL.csv")

    df.to_csv(output, index=False)

    logger.info(f"{symbol} merged | rows={len(df)}")


def merge_all():

    logger.info("Merge started")

    symbols = os.listdir(DATA_DIR)

    for symbol in symbols:
        merge_symbol(symbol)
import os
import pandas as pd

from config import DATA_DIR
from logger import logger


def merge_symbol(symbol):

    folder = os.path.join(DATA_DIR, symbol)

    if not os.path.exists(folder):
        return

    files = [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.endswith(".csv")
    ]

    if not files:
        return

    dfs = []

    for f in files:
        try:
            dfs.append(pd.read_csv(f))
        except Exception as e:
            logger.error(f"{f} read error | {e}")

    df = pd.concat(dfs, ignore_index=True)

    before = len(df)

    # bỏ dòng trùng
    df = df.drop_duplicates()

    after = len(df)

    logger.info(f"{symbol} duplicates removed: {before-after}")

    # sort theo thời gian nếu có cột time
    if "time" in df.columns:
        df = df.sort_values("time")

    output = os.path.join(folder, f"{symbol}_FULL.csv")

    df.to_csv(output, index=False)

    logger.info(f"{symbol} merged | rows={len(df)}")


def merge_all():

    logger.info("Merge started")

    if not os.path.exists(DATA_DIR):
        logger.warning("Data folder not found")
        return

    symbols = os.listdir(DATA_DIR)

    for symbol in symbols:
        merge_symbol(symbol)

    logger.info("Merge finished")


# chạy thủ công
if __name__ == "__main__":

    merge_all()
    logger.info("Merge finished")