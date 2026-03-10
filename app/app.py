from backend import process_excel_file
from frontend import ExcelValidatorUI


def streamlit_app():
    st_ui = ExcelValidatorUI()
    st_ui.display_header()

    upload_file = st_ui.upload_file()

    if upload_file:
        result, errors = process_excel_file(upload_file)
        st_ui.display_result(result, errors)


if __name__ == "__main__":
    streamlit_app()
