# Import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Create empty lists to store the data
product_name_list = []
price_list = []
rating_list = []
review_list = []
description_list = []

# Loop through pages 1 to 20
for page in range(1, 21):
    # Construct the page URL
    url = f"https://webscraper.io/test-sites/e-commerce/static/computers/laptops?page={page}"

    # Fetch the web page
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the data from the page
    product_names = soup.find_all('a', class_='title')
    prices = soup.find_all('h4', class_='pull-right price')
    ratings = soup.find_all('p', {'data-rating': True})
    reviews = soup.find_all('p', class_='pull-right')
    descriptions = soup.find_all('p', class_='description')

    # Add the data to the respective lists
    for name in product_names:
        product_name_list.append(name.text)

    for price in prices:
        price_list.append(price.text)

    for rating in ratings:
        rating_list.append(rating.get('data-rating'))

    for review in reviews:
        review_list.append(review.text)

    for description in descriptions:
        description_list.append(description.text)

# Create a dataframe from the collected data
df = pd.DataFrame({
    'Product Name': product_name_list,
    'Price': price_list,
    'Rating': rating_list,
    'Review': review_list,
    'Description': description_list
})

# Create a CSV file
filepath = "web_scraping/scraped_data.csv"
df.to_csv(filepath, index=False)