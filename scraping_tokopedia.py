# Import libraries
from selenium import webdriver 
from selenium.webdriver.common.by import By
import pandas as pd
import time
from selenium.common.exceptions import NoSuchElementException
import os

# Create an empty list to store the data
data = []

# Configure selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

# Loop through pages 1 to 10
for page in range(1, 4):
    # print status
    print("Please wait, scraping page {}".format(page))

    # Construct the page URL
    url = f"https://www.tokopedia.com/search?navsource=&ob=5&page={page}&q=laptop&srp_component_id=04.06.00.00&srp_page_id=&srp_page_title=&st="

    driver.get(url)

    time.sleep(10)

    # Scraping process
    products = driver.find_elements(By.XPATH, "//div[@class='prd_link-product-name css-3um8ox']")

    for product in products:
        product_name = product.text

        parent = product.find_element(By.XPATH, "..")

        try:
            price_element = parent.find_element(By.XPATH, ".//div[@class='prd_link-product-price css-1ksb19c']")
            price = price_element.text
        except NoSuchElementException:
            price = None

        try:
            location_element = parent.find_element(By.XPATH, ".//span[@class='prd_link-shop-loc css-1kdc32b flip']")
            location = location_element.text
        except NoSuchElementException:
            location = None

        try:
            rating_element = parent.find_element(By.XPATH, ".//span[@class='prd_rating-average-text css-t70v7i']")
            rating = rating_element.text
        except NoSuchElementException:
            rating = None

        try:
            sales_element = parent.find_element(By.XPATH, ".//span[@class='prd_label-integrity css-1duhs3e']")
            sales = sales_element.text
        except NoSuchElementException:
            sales = None

        data.append({
            'Product': product_name,
            'Price': price,
            'Rating': rating,
            'Location': location,
            'Sales': sales,
        })

driver.quit()
print("Scraping process is done.")


# Create a DataFrame from the collected data
df = pd.DataFrame(data)

# Create a CSV file
df.to_csv(os.getcwd() + '\scraped_tokopedia_data.csv', index=False)