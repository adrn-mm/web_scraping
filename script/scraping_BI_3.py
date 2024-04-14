# Import libraries
from selenium import webdriver 
from selenium.webdriver.common.by import By
import pandas as pd
import time
import os
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import subprocess
from datetime import datetime

# define the url
url= "https://www.bi.go.id/id/statistik/informasi-kurs/transaksi-bi/Default.aspx"

# Configure selenium via local driver
# options = webdriver.ChromeOptions()
# options.add_argument("--headless=new")
# driver = webdriver.Chrome(options=options)

# Configure selenium via docker
driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", DesiredCapabilities.FIREFOX)

# print status
print("Please wait, start scraping...")

# solution for timeout
driver.set_page_load_timeout(20)
try:
    driver.get(url)
except TimeoutException:
    driver.execute_script("window.stop();")

# wait for elements to show up
time.sleep(10)

# get the table
table = driver.find_elements(By.CLASS_NAME, 'text-right')

# get the date
date_element = driver.find_element(By.XPATH, '//*[@id="tableData"]/div/div[4]/div[1]/div[1]/div/div')
date_text = date_element.text  
date_str = date_text.replace("Update Terakhir ", "")
date_obj = datetime.strptime(date_str, "%d %B %Y")
date_formatted = date_obj.strftime("%Y%m%d")
print("The date is {}".format(date_formatted))

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
data = [lst_elements[i:i+4] for i in range(5, len(lst_elements), 4)]
df = pd.DataFrame(data, columns=header)
df = df.drop(df.index[-1]) # Menghapus baris terakhir karena isinya tidak digunakan
df['datadt'] = date_formatted

driver.close()

# check if the date.txt file exists
if not os.path.exists('date.txt'):
    # file does not exist, write the date to the file
    with open('date.txt', 'w') as f:
        f.write(date_formatted)

    # save df to csv
    csv_file_name = f'kurs_trx_BI_{date_formatted}.csv'
    df.to_csv(csv_file_name, index=False)

    print(f"Date.txt file did not exist. Created with date {date_formatted}. CSV file has been created.")
else:
    # file exists, read the date from the file
    with open('date.txt', 'r') as f:
        previous_date = f.read().strip()

    # check if the date has changed
    if previous_date != date_formatted:
        # write the new date to the file
        with open('date.txt', 'w') as f:
            f.write(date_formatted)

        # save df to csv
        csv_file_name = f'kurs_trx_BI_{date_formatted}.csv'
        df.to_csv(csv_file_name, index=False)

        print(f"Date has changed to {date_formatted}. CSV file has been created.")
    else:
        print(f"Date is still {date_formatted}. No need to create a new CSV file.")

# Lokasi target di HDFS untuk file JSON
hdfs_directory_path = '/user/user_etl/csv'
hdfs_file_name = csv_file_name

# Mengunggah file csv ke HDFS
subprocess.call(['hadoop', 'fs', '-mkdir', '-p', hdfs_directory_path])
subprocess.call(['hadoop', 'fs', '-put', '-f', hdfs_file_name, f"{hdfs_directory_path}/{hdfs_file_name}"])
print("CSV file successfully added to HDFS")

# Membuat external table di Hive
hive_query = f"""
    CREATE EXTERNAL TABLE IF NOT EXISTS kurs_transaksi_BI (
        "Mata Uang" INT,
        "Nilai" STRING,
        "Kurs Jual" INT,
        "Kurs Beli" STRING
    )
    PARTITIONED BY (datadt STRING)
    ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe'
    STORED AS TEXTFILE
    LOCATION '{hdfs_directory_path}';
    """
hive_cmd = ['hive', '-e', hive_query]

# subprocess.run(hive_cmd, check=True)
print("External table berhasil dibuat di Hive.")