from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from tqdm import tqdm
from numpy import random
import pandas as pd

def init_driver():
    return webdriver.Firefox()

if __name__ == "__main__":
    df = pd.read_csv("kaggle_urls.csv")
    dataset_urls = df['URL'].to_list()[:300]
    dataset_details = []
    iteration_count = 0
    max_iterations = 10

    driver = init_driver()

    for url in tqdm(dataset_urls):
        if iteration_count >= max_iterations:
            driver.quit()
            driver = init_driver()
            iteration_count = 0  # Reset the iteration count

        driver.implicitly_wait(0.5)
        driver.get(url)
        # time.sleep(1)
        time.sleep(random.randint(1,3))

        try:
            title = driver.find_element(By.CLASS_NAME, "sc-jwIPbr").text
        except NoSuchElementException:
            title = None    
        
        try:
            p_elements = driver.find_elements(By.CSS_SELECTOR, 'div.sc-ePpfBx.hvYpEH p')
            details = " ".join([p.text for p in p_elements])
            details = details.replace("\n", "")
        except NoSuchElementException:
            details = None
        
        try:
            tag_elements = driver.find_elements(By.XPATH, '//div[@id="combo-tags-menu-chipset"]//span')
            tags = [tag.text for tag in tag_elements]
        except NoSuchElementException:
            tags = None

        dataset_details.append({
            "title": title,
            "url": url,
            "details": details,
            "tags": tags
        })

        iteration_count += 1  # Increment the iteration counter

    driver.quit()  # Ensure the driver is closed after all operations

    df = pd.DataFrame(data=dataset_details, columns=dataset_details[0].keys())
    df.to_csv("dataset_details.csv", index=False)
