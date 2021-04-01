import time
import progressbar
import logging
from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException,
                                        ElementNotInteractableException)


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
    driver = webdriver.Chrome(executable_path="./chromedriver")
    driver.get("https://scrap.tf/raffles")

    print("Please sign in through STEAM master...")
    input("Is it finished? ")

    print("Starting execution...")

    raffles = get_raffles()
    print(f"Found {len(raffles)} raffles!")
    for raffle in progressbar.progressbar(raffles):
        time.sleep(3)
        enter_raffle(raffle)

    driver.close()
