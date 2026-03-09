from frontend import ExcelValidatorUI


def streamlit_app():
    st_ui = ExcelValidatorUI()
    st_ui.display_header()


if __name__ == "__main__":
    streamlit_app()
