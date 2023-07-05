# Import libraries
from selenium import webdriver 
from selenium.webdriver.common.by import By
import pandas as pd
import time
import os
from selenium.common.exceptions import TimeoutException

# define the url
url= "https://www.bi.go.id/id/statistik/informasi-kurs/transaksi-bi/Default.aspx"

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
table = driver.find_elements(By.CLASS_NAME, 'text-right')

# print status again
print("Scraping finished!")

# get the text from the table
lst_elements = []
for element in table:
    lst_elements.append(element.text)

# remove empty elements
lst_elements = list(filter(bool, lst_elements))

# create df
header = lst_elements[:4]
rows = lst_elements[6:]
data = [lst_elements[i:i+4] for i in range(5, len(lst_elements), 4)]
df = pd.DataFrame(data, columns=header)

# remove last row from df
df = df.drop(df.index[-1])

# save df to csv
df.to_csv(os.getcwd() + '\scraped_BI_3.csv', index=False)
