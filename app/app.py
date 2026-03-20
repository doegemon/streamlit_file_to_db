from backend import process_excel_file, excel_to_sql_db
from frontend import ExcelValidatorUI


def streamlit_app():
    st_ui = ExcelValidatorUI()
    st_ui.display_header()

    upload_file = st_ui.upload_file()

    if upload_file:
        df, result, errors = process_excel_file(upload_file)
        st_ui.display_result(result, errors)

        if errors:
            st_ui.display_error_message()
        elif st_ui.display_save_button():
            excel_to_sql_db(df)
            st_ui.display_success_message()


if __name__ == "__main__":
    streamlit_app()
