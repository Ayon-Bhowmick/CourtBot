from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import concurrent.futures
import threading
import time

MAX_WORKERS = 50
TITLE_XPATH = "/html/body/div[2]/section/div[1]/div[4]/div/center/h3[1]/p"
BODY_XPATH = "/html/body/div[2]/section/div[1]/div[4]/div"

def get_case_links():
    driver = webdriver.Chrome(options=chrome_options)
    while len(year_links) > 0:
        link = year_links.pop()
        driver.get(link)
        case_links_year = driver.find_elements("tag name", "tbody")[3].find_elements("tag name", "a")
        case_links_year = [link.get_attribute("href") for link in case_links_year]
        case_links.extend(case_links_year)
        break
    driver.quit()
    print(f"finished thread {threading.current_thread().name} for years")

def get_case():
    driver = webdriver.Chrome(options=chrome_options)
    while len(case_links) > 0:
        link = case_links.pop()
        driver.get(link)
        title = driver.find_element("xpath", TITLE_XPATH).text
        body = driver.find_element("xpath", BODY_XPATH).text
        body_list = body.split("\n")
        body_list = [line.strip() for line in body_list if " " in line.strip()]
        with open(f"../SupremeCourtCases/{title}.txt", "w") as f:
            f.write("\n".join(body_list[1:]))
        break
    driver.quit()
    print(f"finished thread {threading.current_thread().name} for cases", len(case_links))


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

    # get case links in parallel
    case_links = []
    pool = concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS)
    link_futures = [pool.submit(get_case_links) for _ in range(MAX_WORKERS)]
    concurrent.futures.wait(link_futures, timeout=None,return_when=concurrent.futures.ALL_COMPLETED)

    # get cases in parallel
    case_futures = [pool.submit(get_case) for _ in range(MAX_WORKERS)]
    pool.shutdown(wait=True)
    print(len(os.listdir("../SupremeCourtCases")))
