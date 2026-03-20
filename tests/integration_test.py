import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv(".env")

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


def test_read_data_and_check_schema():
    df = pd.read_sql("SELECT * FROM sales", con=DATABASE_URL)

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
