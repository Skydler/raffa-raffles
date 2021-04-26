import os
import sys
import time
import progressbar
import logging
from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException,
                                        ElementNotInteractableException)

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


def run_raffle_bot():
    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={resource_path(PROFILE_FOLDER)}")
    options.add_argument(r"headless")
    driver = webdriver.Chrome(
        executable_path=resource_path(f"{SELENIUM_FOLDER}/chromedriver"),
        options=options)
    driver.implicitly_wait(5)

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
    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={resource_path(PROFILE_FOLDER)}")
    driver = webdriver.Chrome(
        executable_path=resource_path(f"{SELENIUM_FOLDER}/chromedriver"),
        options=options)
    driver.implicitly_wait(5)

    logging.info("Loading scraptf website")
    driver.get("https://scrap.tf/raffles")

    logging.info("Please login to scraptf")
    input("Press enter when it's ready ^.^\n")
    driver.close()


def scroll_to_end(driver):
    # Wait till page loads
    driver.find_element_by_css_selector(".big-logo")

    for _ in range(3):
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)


def get_raffles(driver):
    css_selector = ".panel-raffle:not(.raffle-entered)"
    raffle_boxes = driver.find_elements_by_css_selector(css_selector)
    raffles = list(map(
        lambda r: r.find_element_by_css_selector(
            ".raffle-name a").get_attribute("href"), raffle_boxes))
    return raffles


def enter_raffle(driver, raffle):
    driver.get(raffle)
    try:
        div_btns = driver.find_element_by_class_name("enter-raffle-btns")
        div_btns.find_element_by_css_selector(
            "button:not(#raffle-enter)").click()
    except (NoSuchElementException, ElementNotInteractableException):
        logging.error("Couldn't find 'Enter raffle' button")
    else:
        subtitle = driver.find_element_by_class_name("subtitle").text
        logging.info(f"Entered to: {subtitle}")


if __name__ == "__main__":
    progressbar.streams.wrap_stderr()
    logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s')

    profile_exists = check_for_profile()
    if profile_exists:
        run_raffle_bot()
    else:
        login()
