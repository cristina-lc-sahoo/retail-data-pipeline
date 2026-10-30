
import csv
import logging
import os
from pathlib import Path

import psycopg2
from psycopg2.extras import execute_values

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=str(LOG_DIR / "etl.log"),
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

TABLES = {
    "products.csv": (
        "products",
        ["id", "range_set", "item_label", "category",
         "unit_cost", "unit_price", "shrink_risk"],
        ["id"],
    ),
    "sales.csv": (
        "sales",
        ["order_id", "date", "product", "quantity",
         "unit_price", "total", "region", "salesperson"],
        ["order_id"],
    ),
    "stores.csv": (
        "stores",
        ["id", "store_set", "store_label", "store_code",
         "opened_on", "shrink_factor"],
        ["id"],
    ),
}


def main():
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="retail_dw",
        user=os.environ.get("PGUSER", os.environ.get("USER")),
    )

    try:
        with conn:
            with conn.cursor() as cur:
                for filename, (table, columns, keys) in TABLES.items():
                    filepath = DATA_DIR / filename

                    with filepath.open(
                        "r", newline="", encoding="utf-8-sig"
                    ) as file:
                        reader = csv.DictReader(file)

                        if reader.fieldnames != columns:
                            raise ValueError(
                                f"{filename}: unexpected CSV headers "
                                f"{reader.fieldnames}"
                            )

                        rows = [
                            tuple(row[c] or None for c in columns)
                            for row in reader
                        ]

                    column_sql = ", ".join(f'"{c}"' for c in columns)
                    key_sql = ", ".join(f'"{c}"' for c in keys)
                    update_columns = [c for c in columns if c not in keys]

                    if update_columns:
                        updates_sql = ", ".join(
                            f'"{c}" = EXCLUDED."{c}"'
                            for c in update_columns
                        )
                        conflict_sql = (
                            f"ON CONFLICT ({key_sql}) "
                            f"DO UPDATE SET {updates_sql}"
                        )
                    else:
                        conflict_sql = (
                            f"ON CONFLICT ({key_sql}) DO NOTHING"
                        )

                    sql = (
                        f'INSERT INTO raw."{table}" ({column_sql}) '
                        f"VALUES %s {conflict_sql}"
                    )

                    if rows:
                        execute_values(cur, sql, rows, page_size=500)

                    message = (
                        f"{filename}: processed {len(rows)} rows "
                        f"into raw.{table}"
                    )
                    print(message)
                    logging.info(message)

        print("ETL completed successfully.")
        logging.info("ETL completed successfully.")

    except Exception:
        logging.exception("ETL failed")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()

