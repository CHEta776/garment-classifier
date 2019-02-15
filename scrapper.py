from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
import sys
import argparse
from downloader import download_urls


def main(args):

    # Init selenium driver
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options, executable_path=r'./chromedriver')

    image_url_list = []
    base_url = 'https://www.zalando.es/ropa-de-mujer/?p={}'
    i = 2
    image_counter = 0


    # Prepare output folder
    base_folder = args.base_folder
    output_file = 'data.csv'

    if not os.path.exists(base_folder):
        os.makedirs(base_folder)


    while 1:
        new_url = base_url.format(i)
        driver.get(new_url)
        current_url = driver.current_url

        x = driver.find_elements_by_css_selector('div.cat_articleContain-1Z60A')
        garments = [link.find_element_by_css_selector('a').get_attribute('href') for link in x]

        for garment in garments:
            if image_counter == args.n_images:
                break

            # Get url for specific garment
            html_details = requests.get(garment)
            # Access url
            details_soup = BeautifulSoup(html_details.text, 'html.parser')
            # Get all images
            pictures = details_soup.find_all('img', class_='h-image-img h-flex-auto responsive')
            # Look for zoom images
            garment_urls = [pic['src'].replace('thumb', 'zoom') for pic in pictures if 'packshot/pdp-thumb' in pic['src']]

            # Get only first one if exists
            if garment_urls:
                image_url_list.append(garment_urls[0])
                image_counter += 1

        # Save to csv file
        if not i % 2 or image_counter == args.n_images:
            tmp_data = pd.DataFrame(image_url_list, columns=['url'])

            with open(os.path.join(base_folder, output_file), 'a' if i > 2 else 'w') as f:
                tmp_data.to_csv(f, header=(i == 2))

        if new_url != current_url:
            print('This page does not exist: {}'.format(new_url))
            print('You have been redirected to main page (images also downloaded)')
            break

        i += 1
        print('Total pages: {}'.format(i-2))

        if image_counter == args.n_images:
            driver.close()
            break


    # Download obtained urls
    download_urls(base_folder, args.threads)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_folder', '-bf', help='Base folder for downloaded images', type=str, default='Data/')
    parser.add_argument('--n_images', '-n', help='Number of images to download', type=int, default=100)
    parser.add_argument('--threads', '-t', help='Number of threads to use', type=int, default=10)
    args = parser.parse_args()

    main(args)
