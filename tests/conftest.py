import sys
from pathlib import Path

# Add the parent directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.urban_routes_page import UrbanRoutesPage


@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def routes_page(driver):
    page = UrbanRoutesPage(driver)
    page.navigate_to_urban_routes()
    return page
