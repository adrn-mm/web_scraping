# Import libraries
from selenium import webdriver 
from selenium.webdriver.common.by import By
import pandas as pd
import time
import os
from selenium.common.exceptions import TimeoutException

# define the url
url= "https://www.bi.go.id/id/statistik/indikator/bi-7day-rr.aspx"

# Configure selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

# print status
print("Please wait, start scraping...")

# solution for timeout
driver.set_page_load_timeout(10)
try:
    driver.get(url)
except TimeoutException:
    driver.execute_script("window.stop();")

# wait for elements to show up
time.sleep(5)

# get the table
table = driver.find_elements(By.CLASS_NAME, 'text-center')

# print status again
print("Scraping finished!")

# get the href from the table elements
hrefs = []
for element in table:
    link_elements = element.find_elements(By.TAG_NAME, 'a')
    for link_element in link_elements:
        href = link_element.get_attribute('href')
        hrefs.append(href)

# get the text from the table
texts = []
for element in table:
    texts.append(element.text)

# create df
header = texts[:4]
data = [texts[i:i+4] for i in range(4, len(texts), 4)]
df = pd.DataFrame(data, columns=header)

# Change the content of the column
df['Pranala Siaran Pers'] = hrefs

# save df to csv
df.to_csv(os.getcwd() + '\data\scraped_BI_1.csv', index=False)