import os
import pandas as pd
import pytest
from dotenv import load_dotenv

load_dotenv(".env")

POSTGRES_CONFIG = {
    "POSTGRES_USER": os.getenv("POSTGRES_USER"),
    "POSTGRES_PASSWORD": os.getenv("POSTGRES_PASSWORD"),
    "POSTGRES_HOST": os.getenv("POSTGRES_HOST"),
    "POSTGRES_PORT": os.getenv("POSTGRES_PORT"),
    "POSTGRES_DB": os.getenv("POSTGRES_DB"),
}


def test_read_data_and_check_schema():
    missing_vars = [key for key, value in POSTGRES_CONFIG.items() if not value]
    if missing_vars:
        pytest.skip(
            "Skipping PostgreSQL integration test because these env vars are missing: "
            + ", ".join(missing_vars)
        )

    database_url = (
        "postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        "@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    ).format(**POSTGRES_CONFIG)

    df = pd.read_sql("SELECT * FROM sales", con=database_url)

    assert not df.empty, "The table is empty."

    expected_dtype = {
        "customer_email": "object",
        "order_date": "datetime64[ns]",
        "order_value": "float64",
        "product": "object",
        "quantity": "int64",
        "category": "object",
    }

    print(df.dtypes.to_dict())

    assert (
        df.dtypes.to_dict() == expected_dtype
    ), "The table schema doesn't match the expected schema."
