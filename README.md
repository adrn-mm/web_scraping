# Web Scraping Script
## Project Description
Pada project ini saya melakukan proses scraping pada website Bank Indonesia & Tokopedia. Karena kedua website tersebut adalah dynamic dan menggunakan JavaScript, tidak cukup menggunakan library Requests dan BeautifulSoup saja untuk melakukan scraping. Sehingga pada project ini saya menggunakan library Selenium untuk melakukan scraping. Scraping menggunakan library Selenium membutuhkan suatu driver yang sesuai dengan browser yang akan digunakan untuk scraping.
# Scraped Data Description
- scraped_BI_1.csv: BI 7-day (Reverse) Repo Rate
- scraped_BI_2.csv: JISDOR
- scraped_BI_3.csv: data kurs transaksi Bank Indonesia
# File Tree
```
Repository
│   .gitignore
│   explore.ipynb
│   README.md
│   project_report.docx
│   requirements.txt
│
├───data
│       scraped_BI_1.csv
│       scraped_BI_2.csv
│       scraped_BI_3.csv
│       scraped_tokopedia_data.csv
│
└───script
        scraping_BI_1.py
        scraping_BI_2.py
        scraping_BI_3.py
        scraping_tokopedia.py
```