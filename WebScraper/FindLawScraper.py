from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import concurrent.futures
import threading

if __name__ == "__main__":
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("log-level=3")
    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://caselaw.findlaw.com/court/us-supreme-court/years")
    year_links = driver.find_element("id", "brwsopncal").find_elements("tag name", "a")
    year_links = [link.get_attribute("href") for link in year_links]
    