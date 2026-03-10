import pandas as pd
from data_contract import Orders


def process_excel_file(file_uploaded):
    """ """
    try:
        xls_df = pd.read_excel(file_uploaded)
        errors = []

        # Checking if there are more columns in the file than the expected ones
        extra_cols = set(xls_df.columns) - set(Orders.model_fields.keys())
        if extra_cols:
            return False, [
                "Additional columns detected in the Excel file: "
                + ", ".join(sorted(extra_cols))
            ]

        # Validating each row
        for index, row in xls_df.iterrows():
            try:
                _ = Orders(**row.to_dict())
            except Exception as e:
                errors.append(f"Error on line {index + 2}: {e}")

        return True, errors

    except Exception as e:
        return False, [f"Unexpected error: {str(e)}"]
