from selenium import webdriver
import time

driver = webdriver.Chrome(executable_path="./chromedriver")
driver.get("https://scrap.tf/raffles")

print("Please sign in through STEAM master...")
input("Is it finished? ")


def get_raffles():
    css_selector = ".panel-raffle:not(.raffle-entered)"
    raffle_boxes = driver.find_elements_by_css_selector(css_selector)
    raffles = list(map(
        lambda r: r.find_element_by_css_selector(
            ".raffle-name a").get_attribute("href"), raffle_boxes))
    return raffles


def enter_raffle(raffle):
    driver.get(raffle)
    div_btns = driver.find_element_by_class_name("enter-raffle-btns")
    btn = div_btns.find_element_by_css_selector("button:not(#raffle-enter)")
    btn.click()


raffles = get_raffles()
for raffle in raffles:
    time.sleep(3)
    enter_raffle(raffle)

driver.close()
