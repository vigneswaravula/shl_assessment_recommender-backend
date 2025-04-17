from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import json
import os

def scrape_assessments(save_path="app/data/assessments.json"):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    results = []

    for type_id in [1, 2, 3]:  # <-- Line 11
        url = f"https://www.shl.com/solutions/products/product-catalog/?start=0&type={type_id}"
        driver.get(url)  # <-- Line 13

        while True:
            time.sleep(2)  # wait for page to load


    results = []
    while True:
        time.sleep(2)  # wait for page to load

        rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        if not rows:
            break

        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) < 4:
                continue

            name_tag = cols[0].find_element(By.TAG_NAME, "a")
            name = name_tag.text.strip()
            link = name_tag.get_attribute("href")
            remote = "Yes" if "green" in cols[1].get_attribute("innerHTML") else "No"
            adaptive = "Yes" if "green" in cols[2].get_attribute("innerHTML") else "No"
            code_map = {
                "A": "Ability",
                "B": "Behavioral",
                "C": "Cognitive",
                "K": "Knowledge",
                "P": "Personality",
                "S": "Skills"
            }

            raw_type = cols[3].text.strip()
            test_type = " ".join(code_map.get(c, c) for c in raw_type)


            results.append({
                "name": name,
                "url": link,
                "remote_support": remote,
                "adaptive_support": adaptive,
                "type": test_type
            })

        # Try to go to next page
        next_button = driver.find_elements(By.LINK_TEXT, str(len(results)//10 + 2))
        if next_button:
            next_button[0].click()
        else:
            break

    driver.quit()

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"✅ Scraped {len(results)} assessments to {save_path}")
