from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from chromedriver_py import binary_path
from selenium.common.exceptions import StaleElementReferenceException

import os
import time
import requests


class Scrapper:

    def __init__(self, query, number_images, format, min_dimension, verbose=True):
        self.query = query
        self.number_images = number_images
        self.format = format
        self.min_dimension = min_dimension
        self.verbose = verbose

    def webdriver_init(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Запуск в безголовом режиме

        svc = webdriver.ChromeService(executable_path=binary_path)
        driver = webdriver.Chrome(service=svc)

        driver.maximize_window()

        return driver

    def retrieve_image(self, url, image_number, output_dir):

        response = requests.get(url)
        if response.status_code == 200:
            with open(f'./{output_dir}/{image_number}.{self.format}', 'wb') as f:
                f.write(response.content)
        else:
            print(f"Loading error: {response.status_code}")

    def download_images(self):

        driver = self.webdriver_init()

        for query in self.query:

            print('-----------------------------------')

            if not os.path.exists(query):
                os.makedirs(query)
                print(f'Directory /{query}/ created')
            else:
                print(f'Directory /{query}/ exists')

            print('-----------------------------------')

            driver.get(f"https://unsplash.com/s/photos/{query}?license=free")

            time.sleep(2)

            image_number = 0
            urls = []

            while image_number < self.number_images:

                images = driver.find_elements(By.TAG_NAME, 'img')
                time.sleep(2)

                for img in images:
                    try:
                        src = img.get_attribute('src')
                        data_src = img.get_attribute('data-src')
                        srcset = img.get_attribute('srcset')

                        width = img.get_attribute('width')
                        height = img.get_attribute('height')

                        image_url = None

                        if width and height and int(width) > self.min_dimension and int(height) > self.min_dimension:
                            if src and 'https' in src:
                                image_url = src
                            elif data_src and 'https' in data_src:
                                image_url = data_src
                            elif srcset:
                                image_url = srcset.split(',')[0].split(' ')[0]
                        else:
                            continue

                        if image_url and image_url not in urls:
                            self.retrieve_image(image_url, image_number, query)
                            if self.verbose:
                                print(f'Directory /{query}/ , image {image_number} downloaded')
                            image_number += 1
                            urls.append(image_url)

                        if image_number == self.number_images:
                            break

                    except StaleElementReferenceException:
                        print(f"The element is out of date, skip it")

                if image_number == self.number_images:
                    break

                try:
                    explore_button = driver.find_element(By.XPATH, '//button[text()="Load more"]')
                    explore_button.click()
                    # print("The button 'Load more' is pressed")
                except:
                    # print("The 'Load more' button is not visible on the page.")
                    pass

                driver.execute_script("window.scrollBy(0,1000)")

        driver.quit()

        print('-----------------------------------')

        print("Download complete")
