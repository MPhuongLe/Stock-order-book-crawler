import os
import pandas as pd

from config import DATA_DIR
from logger import logger


def merge_symbol(symbol):

    raw_root = os.path.join(DATA_DIR, symbol, "raw")

    if not os.path.exists(raw_root):
        return

    dates = os.listdir(raw_root)

    for date in dates:

        raw_folder = os.path.join(raw_root, date)

        files = [
            os.path.join(raw_folder, f)
            for f in os.listdir(raw_folder)
            if f.endswith(".csv")
        ]

        if not files:
            continue

        dfs = []

        for f in files:
            try:
                dfs.append(pd.read_csv(f))
            except Exception as e:
                logger.error(f"{f} read error | {e}")

        if not dfs:
            continue

        df = pd.concat(dfs, ignore_index=True)

        before = len(df)

        # drop duplicate
        df = df.drop_duplicates(
            subset=["time","price","volume", "id"],
            keep="last"
        )

        after = len(df)

        logger.info(f"{symbol} {date} duplicates removed: {before-after}")

        # sort nếu có time
        if "time" in df.columns:
            df = df.sort_values("time")

        merged_dir = os.path.join(DATA_DIR, symbol, "merged", date)
        os.makedirs(merged_dir, exist_ok=True)

        output = os.path.join(merged_dir, f"{symbol}-{date}.csv")

        df.to_csv(output, index=False)

        logger.info(f"{symbol} {date} merged | rows={len(df)}")


def merge_all():

    logger.info("Merge started")

    if not os.path.exists(DATA_DIR):
        logger.warning("Data folder not found")
        return

    symbols = os.listdir(DATA_DIR)

    for symbol in symbols:
        merge_symbol(symbol)

    logger.info("Merge finished")


if __name__ == "__main__":
    merge_all()