from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import concurrent.futures
import threading
import time

MAX_WORKERS = 1

def get_cases():
    while len(year_links) > 0:
        link = year_links.pop()
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(link)
        case_links = driver.find_elements("tag name", "tbody")[3].find_elements("tag name", "a")
        case_links = [link.get_attribute("href") for link in case_links]
        print(case_links)


if __name__ == "__main__":
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("log-level=3")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-errors")
    chrome_options.add_argument("--ignore-certificate-errors-spki-list")

    # Get all year links
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://caselaw.findlaw.com/court/us-supreme-court/years")
    year_links = driver.find_element("id", "brwsopncal").find_elements("tag name", "a")
    year_links = [link.get_attribute("href") for link in year_links]
    driver.quit()

    # get cases in parallel
    pool = concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS)
    for i in range(MAX_WORKERS):
        pool.submit(get_cases)
    pool.shutdown(wait=True)
