from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from tqdm import tqdm
# from numpy import random
import pandas as pd
import os


if __name__ == "__main__":
    driver = webdriver.Edge()
    urls=[]
    
    for page_no in tqdm(range(1,501)):
        page_url= f"https://www.kaggle.com/datasets?sort=votes&page={page_no}"
        driver.get(page_url)
        time.sleep(3)
        try:
            # Locate all potential list items
            list_items = driver.find_elements(By.CLASS_NAME, "MuiListItem-root")

            for item in list_items:
                try:
                    # Check if the <a> tag has a valid href containing '/datasets/'
                    url_element = item.find_element(By.CSS_SELECTOR, "a[role='link']")
                    url = url_element.get_attribute("href")
                    
                    # Only process items with '/datasets/' in the URL
                    if "/datasets/" in url:
                        # Extract the label from the nested div
                        label_element = item.find_element(By.CSS_SELECTOR, "div.sc-eauhAA.sc-fXwCOG")
                        label = label_element.text
                        urls.append((label, url))


                except Exception:
                    # Skip items that don't match the dataset pattern
                    continue

        except Exception as e:
            print("An error occurred:", e)
            
    df = pd.DataFrame(urls, columns=["Label", "URL"])
    df.to_csv("kaggle_datasets.csv", index=False)
