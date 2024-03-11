import csv
from typing import List
from config import settings


def write_data_to_csv(path: str, rows: List[tuple], headers: tuple) -> None:
    with open(path, "w", encoding="utf-8", newline="") as csv_file:
        settings.stream_logger.debug(msg="WRITING IS STARTED")
        writer = csv.writer(csv_file, delimiter=";")
        writer.writerow(
            headers
        )

        writer.writerows(rows)
