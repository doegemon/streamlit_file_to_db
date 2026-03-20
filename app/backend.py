import os
import pandas as pd
from data_contract import Orders
from dotenv import load_dotenv

load_dotenv(".env")

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


def process_excel_file(file_uploaded):
    """ """
    try:
        xls_df = pd.read_excel(file_uploaded)
        errors = []

        # Checking if there are more columns in the file than the expected ones
        extra_cols = set(xls_df.columns) - set(Orders.model_fields.keys())
        if extra_cols:
            return (
                xls_df,
                False,
                [
                    "Additional columns detected in the Excel file: "
                    + ", ".join(sorted(extra_cols))
                ],
            )

        # Validating each row
        for index, row in xls_df.iterrows():
            try:
                _ = Orders(**row.to_dict())
            except Exception as e:
                errors.append(f"Error on line {index + 2}: {e}")

        return xls_df, True, errors

    except Exception as e:
        return xls_df, False, [f"Unexpected error: {str(e)}"]


def excel_to_sql_db(df):
    """ """
    df.to_sql("sales", con=DATABASE_URL, if_exists="replace", index=False)
