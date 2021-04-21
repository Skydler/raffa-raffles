import time
import progressbar
import logging
from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException,
                                        ElementNotInteractableException)


def scroll_to_end():
    # Wait till page loads
    driver.find_element_by_css_selector(".big-logo")

    for _ in range(3):
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)


def get_raffles():
    css_selector = ".panel-raffle:not(.raffle-entered)"
    raffle_boxes = driver.find_elements_by_css_selector(css_selector)
    raffles = list(map(
        lambda r: r.find_element_by_css_selector(
            ".raffle-name a").get_attribute("href"), raffle_boxes))
    return raffles


def enter_raffle(raffle):
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

    options = webdriver.ChromeOptions()
    options.add_argument(r"--user-data-dir=./selenium/selenium_chrome_profile")
    driver = webdriver.Chrome(
        executable_path="./selenium/chromedriver", options=options)
    driver.implicitly_wait(5)

    driver.get("https://scrap.tf/raffles")
    scroll_to_end()
    print("Starting execution...")
    raffles = get_raffles()
    print(f"Found {len(raffles)} raffles!")
    for raffle in progressbar.progressbar(raffles):
        time.sleep(3)
        enter_raffle(raffle)

    driver.close()
