import os
import sys
import time
import progressbar
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotInteractableException,
)
from webdriver_manager.chrome import ChromeDriverManager

SELENIUM_FOLDER = "./selenium"
PROFILE_FOLDER = f"{SELENIUM_FOLDER}/selenium_chrome_profile"


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)


def check_for_profile():
    try:
        with open(resource_path(f"{PROFILE_FOLDER}/First Run"), "r"):
            has_file = True
    except IOError:
        logging.warning("Chrome profile not found")
        has_file = False

    return has_file


def build_driver(headless=True, silent=True):
    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={resource_path(PROFILE_FOLDER)}")
    if headless:
        options.add_argument("--headless")

    if silent:
        options.add_argument("--disable-crash-reporter")
        options.add_argument("--disable-in-process-stack-traces")
        options.add_argument("--disable-logging")
        options.add_argument("--log-level=3")

    driver = webdriver.Chrome(
        executable_path=ChromeDriverManager().install(),
        options=options,
    )
    driver.implicitly_wait(5)

    return driver


def run_raffle_bot():
    driver = build_driver()
    logging.info("Loading scraptf website")
    driver.get("https://scrap.tf/raffles")

    logging.info("Scrolling to the end of the webpage...")
    scroll_to_end(driver)

    logging.info("Starting execution...")
    raffles = get_raffles(driver)

    logging.info(f"Found {len(raffles)} raffles!")
    for raffle in progressbar.progressbar(raffles):
        time.sleep(3)
        enter_raffle(driver, raffle)

    driver.close()


def login():
    driver = build_driver(headless=False)
    logging.info("Loading scraptf website")
    driver.get("https://scrap.tf/raffles")

    logging.info("Please login to scraptf")
    input("Press enter when it's ready ^.^\n")
    driver.close()


def scroll_to_end(driver):
    # Wait till page loads
    driver.find_element(By.CSS_SELECTOR, ".big-logo")

    for _ in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)


def get_raffles(driver):
    css_selector = ".panel-raffle:not(.raffle-entered)"
    raffle_boxes = driver.find_elements(By.CSS_SELECTOR, css_selector)
    raffles = list(
        map(
            lambda r: r.find_element(By.CSS_SELECTOR, ".raffle-name a").get_attribute(
                "href"
            ),
            raffle_boxes,
        )
    )
    return raffles


def enter_raffle(driver, raffle):
    driver.get(raffle)
    try:
        div_btns = driver.find_element(By.CSS_SELECTOR, ".enter-raffle-btns")
        div_btns.find_element(By.CSS_SELECTOR, "button:not(#raffle-enter)").click()
    except (NoSuchElementException, ElementNotInteractableException):
        logging.error("Couldn't find 'Enter raffle' button")
    else:
        subtitle = driver.find_element(By.CSS_SELECTOR, ".subtitle").text
        logging.info(f"Entered to: {subtitle}")


if __name__ == "__main__":
    progressbar.streams.wrap_stderr()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")

    profile_exists = check_for_profile()
    if profile_exists:
        run_raffle_bot()
    else:
        login()
