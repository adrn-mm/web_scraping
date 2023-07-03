"""
This script still on development

"""


import csv
from selenium import webdriver
from selenium.webdriver.common.by import By

# Configure selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

# Navigate to the website
driver.get("https://www.bi.go.id/id/statistik/informasi-kurs/transaksi-bi/Default.aspx")

# Wait for the table to be visible
table = driver.find_element(By.XPATH, "//*[@id="ctl00_PlaceHolderMain_g_6c89d4ad_107f_437d_bd54_8fda17b556bf_ctl00_GridView1"]/table")

# Get the HTML content of the table
table_html = table.get_attribute("innerHTML")

# Close the browser
driver.quit()

# Process the table HTML content using Beautiful Soup or other methods
# Example: Use Beautiful Soup to parse the table
from bs4 import BeautifulSoup
soup = BeautifulSoup(table_html, "html.parser")

# Find all table rows
rows = soup.find_all("tr")

# Extract data from the table rows and store in a list of lists
data = []
for row in rows:
    # Get data from table cells
    cells = row.find_all("td")
    row_data = [cell.text for cell in cells]
    data.append(row_data)

# Write the data to a CSV file
with open("output.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)

print("Data saved to output.csv")