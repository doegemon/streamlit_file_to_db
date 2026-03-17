import pytest
import subprocess
from time import sleep, time
from urllib.error import URLError
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait


APP_URL = "http://localhost:8501"


def wait_for_app(url, timeout=20):
    """Wait until the Streamlit app responds before opening the browser."""
    deadline = time() + timeout
    while time() < deadline:
        try:
            with urlopen(url, timeout=2) as response:
                if response.status == 200:
                    return
        except URLError:
            sleep(1)

    raise TimeoutError(f"Timed out waiting for {url}")


@pytest.fixture
def driver():
    """Start the app and return a headless Firefox WebDriver."""
    process = subprocess.Popen(
        [
            "poetry",
            "run",
            "streamlit",
            "run",
            "app/app.py",
            "--server.headless=true",
        ]
    )
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)
    browser.set_page_load_timeout(10)

    try:
        wait_for_app(APP_URL)
        yield browser
    finally:
        browser.quit()
        process.kill()
        process.wait(timeout=5)


def test_app_open(driver):
    """The app should open successfully."""
    driver.get(APP_URL)
    sleep(5)
    WebDriverWait(driver, 10).until(lambda current_driver: current_driver.title != "")


def test_check_title(driver):
    """The page title should match the configured Streamlit title."""
    driver.get(APP_URL)
    sleep(3)
    WebDriverWait(driver, 10).until(lambda current_driver: current_driver.title != "")

    page_title = driver.title

    expected_title = "Excel Schema Validator"
    assert page_title == expected_title


def test_check_header(driver):
    """The page header should render the expected text."""
    driver.get(APP_URL)
    sleep(3)
    WebDriverWait(driver, 10).until(
        lambda current_driver: current_driver.find_element(By.TAG_NAME, "h1").text != ""
    )

    header_element = driver.find_element(By.TAG_NAME, "h1")

    expected_text = "Excel Schema Validator"
    assert header_element.text == expected_text
