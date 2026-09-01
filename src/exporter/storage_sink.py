import os
import pandas as pd
from typing import List
from src.parser.tweet_extractor import TweetRecord

class StorageSink:
    @staticmethod
    def export_to_parquet_and_csv(records: List[TweetRecord], output_dir: str = "data/processed"):
        os.makedirs(output_dir, exist_ok=True)
        if not records:
            print("No records to export.")
            return

        data = [r.model_dump() for r in records]
        for item in data:
            item["image_urls"] = ", ".join(item["image_urls"]) if item["image_urls"] else ""

        df = pd.DataFrame(data)
        csv_path = os.path.join(output_dir, "feed_data.csv")
        parquet_path = os.path.join(output_dir, "feed_data.parquet")

        df.to_csv(csv_path, index=False)
        df.to_parquet(parquet_path, index=False)
        print(f"Data Sink Completed: {len(df)} records stored in CSV and Parquet.")