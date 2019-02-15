from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import pandas as pd
import os

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options, executable_path=r'./chromedriver')

image_url_list = []
base_url = 'https://www.zalando.es/ropa-de-mujer/?p={}'
i = 2


# Prepare output folder
base_folder = 'Data/'
if not os.path.exists(base_folder):
    os.makedirs(base_folder)

while 1:
    new_url = base_url.format(i)
    driver.get(new_url)
    current_url = driver.current_url

    x = driver.find_elements_by_css_selector("div.cat_articleContain-1Z60A")
    garments = [link.find_element_by_css_selector('a').get_attribute('href') for link in x]

    for garment in garments:
        # Get url for specific garment
        html_details = requests.get(garment)
        # Access url
        details_soup = BeautifulSoup(html_details.text, 'html.parser')
        # Get all images
        pictures = details_soup.find_all("img", class_='h-image-img h-flex-auto responsive')
        # Look for zoom images
        garment_urls = [pic['src'].replace('thumb', 'zoom') for pic in pictures if 'packshot/pdp-thumb' in pic['src']]

        # Get only first one if exists
        if garment_urls:
            image_url_list.append(garment_urls[0])

    # Save to csv file
    if not i % 2:
        tmp_data = pd.DataFrame(image_url_list, columns=['url'])

        with open(os.path.join(base_folder,'data.csv'), 'a') as f:
            tmp_data.to_csv(f, header=(i == 2))

    if new_url != current_url:
        print('This page does not exist: {}'.format(new_url))
        print('Redirected to main page (images also downloaded)')
        break

    print('Total pages: {}'.format(i-2))

    i+=1

