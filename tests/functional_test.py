import pytest
import subprocess
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


@pytest.fixture
def driver():
    """ """
    process = subprocess.Popen(["poetry", "run", "streamlit", "run", "app/app.py"])
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.set_page_load_timeout(5)
    yield driver

    driver.quit()
    process.kill()


def test_app_open(driver):
    """ """
    driver.get("http://localhost:8501")
    sleep(5)


def test_check_title(driver):
    """ """
    driver.get("http://localhost:8501")
    sleep(3)

    page_title = driver.title

    expected_title = "Excel Schema Validator"
    assert page_title == expected_title


def test_check_header(driver):
    """ """
    driver.get("http://localhost:8501")
    sleep(3)

    header_element = driver.find_element(By.TAG_NAME, "h1")

    expected_text = "Excel Schema Validator"
    assert header_element.text == expected_text
