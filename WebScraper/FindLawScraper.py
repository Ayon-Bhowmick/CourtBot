from selenium import webdriver
import os
import concurrent.futures
import threading
import time
import re

MAX_WORKERS = 500
MIN_LINE_LENGTH = 16
TITLE_XPATH = "/html/body/div[2]/section/div[1]/div[3]/div/center/h3[1]/p"
BODY_XPATH = "/html/body/div[2]/section/div[1]/div[3]/div"
FOOTNOTE_REGEX = r"^[Ff]ootnote\s{0,}\d{0,}$"
TEXT_REGEX = r"[\w\d]{1,}"

def line_check(line: str) -> bool:
    line = line.strip()
    ret = True and (" " in line)
    ret = ret and not bool(re.search(FOOTNOTE_REGEX, line))
    ret = ret and bool(re.search(TEXT_REGEX, line))
    ret = ret and (len(line.split()) >= MIN_LINE_LENGTH)
    return ret

def get_case_links():
    print(f"starting thread {threading.current_thread().name} for years")
    driver = webdriver.Chrome(options=chrome_options)
    while len(year_links) > 0:
        link = year_links.pop()
        driver.get(link)
        case_links_year = driver.find_elements("tag name", "tbody")[3].find_elements("tag name", "a")
        case_links_year = [link.get_attribute("href") for link in case_links_year]
        case_links.extend(case_links_year)
    driver.quit()
    print(f"finished thread {threading.current_thread().name} for years {len(year_links)} years left")

def get_case():
    print(f"starting thread {threading.current_thread().name} for cases")
    driver = webdriver.Chrome(options=chrome_options)
    while len(case_links) > 0:
        link = case_links.pop()
        driver.get(link)
        title = driver.find_element("xpath", TITLE_XPATH).text
        body = driver.find_element("xpath", BODY_XPATH).text
        body_list = body.split("\n")
        body_list = ["".join([i if ord(i) < 128 else "" for i in line.strip()]) for line in body_list if line_check(line)]
        with open(f"../SupremeCourtCases/{title}.txt", "w") as f:
            f.write("\n".join(body_list[1:]))
    driver.quit()
    print(f"finished thread {threading.current_thread().name} for cases {len(case_links)} cases left")


if __name__ == "__main__":
    start = time.time()
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
    concurrent.futures.wait(link_futures, timeout=None, return_when=concurrent.futures.ALL_COMPLETED)
    print(f"\nyears left: {len(year_links)}\ncases left: {len(case_links)}\n")

    # get cases in parallel
    jank = -1
    while len(case_links) > 0:
        jank += 1
        case_futures = [pool.submit(get_case) for _ in range(MAX_WORKERS)]
        concurrent.futures.wait(case_futures, timeout=None, return_when=concurrent.futures.ALL_COMPLETED)
        print(f"\ncases left: {len(case_links)}\ncases downloaded: {len(os.listdir('../SupremeCourtCases'))} with jank count {jank}\n")
    pool.shutdown(wait=True)

    seconds = time.time() - start
    minutes = seconds // 60
    seconds = seconds - minutes * 60
    hours = minutes // 60
    minutes = minutes - hours * 60
    print(f"Total time: {int(hours)}:{int(minutes)}:{seconds}")
