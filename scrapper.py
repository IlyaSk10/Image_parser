from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from chromedriver_py import binary_path
from selenium.common.exceptions import StaleElementReferenceException

import os
import time
import requests

query = "laptop"
folder_name = query
format = "png"
N_total = 77


class Scrapper:

    def __init__(self, query, output_dir, number_images, format):
        self.query = query
        self.output_dir = output_dir
        self.number_images = number_images
        self.format = format

    def webdriver_init(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # optional
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        svc = webdriver.ChromeService(executable_path=binary_path)
        driver = webdriver.Chrome(service=svc)

        driver.get(f"https://unsplash.com/s/photos/{self.query}?license=free")
        driver.maximize_window()

        return driver

    def download_image(self, url, image_number):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        response = requests.get(url)
        if response.status_code == 200:
            with open(f'./{self.output_dir}/{image_number}.{self.format}', 'wb') as f:
                f.write(response.content)
        else:
            print(f"Loading error: {response.status_code}")

    def get_url(self):

        driver = self.webdriver_init()

        time.sleep(3)

        image_number = 0

        while image_number < self.number_images:

            images = driver.find_elements(By.TAG_NAME, 'img')

            for i in range(len(images)):
                try:
                    img = images[i]
                    src = img.get_attribute('src')
                    data_src = img.get_attribute('data-src')
                    srcset = img.get_attribute('srcset')

                    width = img.get_attribute('width')
                    height = img.get_attribute('height')

                    image_url = None

                    if width and height and int(width) > 100 and int(height) > 100:
                        if src and 'https' in src:
                            image_url = src
                        elif data_src and 'https' in data_src:
                            image_url = data_src
                        elif srcset:
                            image_url = srcset.split(',')[0].split(' ')[0]
                    elif src and src.startswith('data:image/'):
                        continue
                    else:
                        continue

                    if image_url:
                        self.download_image(image_url, image_number)
                        image_number += 1

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
                continue

            driver.execute_script("window.scrollBy(0,1000)")

        driver.quit()

        print("Download complete")


obj = Scrapper(query=query, output_dir=folder_name, number_images=N_total, format=format)
obj.get_url()
