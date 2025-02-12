from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from chromedriver_py import binary_path
from selenium.common.exceptions import StaleElementReferenceException

import os
import time
import requests
import urllib

folder_name = 'images'


# Функция для загрузки изображения
def download_image(url, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

    response = requests.get(url)
    if response.status_code == 200:
        # Получаем имя файла из URL
        filename = os.path.join(folder, url.split('/')[-1])
        with open(filename, 'wb') as f:
            f.write(response.content)
    else:
        print(f"Ошибка загрузки: {response.status_code}")


start = time.time()
# Настройка опций для Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # (опционально) работа в headless режиме
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Создание экземпляра драйвера
svc = webdriver.ChromeService(executable_path=binary_path)
driver = webdriver.Chrome(
    service=svc
)

# Открытие страницы Unsplash
query = "laptop"  # Замените на ваш запрос
# driver.get(f"https://unsplash.com/s/photos/{query}")
driver.get(f"https://unsplash.com/s/photos/{query}?license=free")

time.sleep(3)  # Дождитесь полной загрузки страницы

print(time.time() - start)
N_total = 33
count = 0

while count < N_total:

    # Получение всех изображений
    images = driver.find_elements(By.TAG_NAME, 'img')

    for i in range(len(images)):
        try:
            img = images[i]
            src = img.get_attribute('src')
            data_src = img.get_attribute('data-src')
            srcset = img.get_attribute('srcset')

            # Выбираем URL изображения
            image_url = None
            if src and 'https' in src:
                width = img.get_attribute('width')
                height = img.get_attribute('height')
                if width and height and int(width) > 100 and int(height) > 100:
                    image_url = src
                    # print(i, image_url)
                else:
                    # print(i, 'crop')
                    continue
            elif data_src and 'https' in data_src:
                image_url = data_src
                # print(i, image_url)
            elif srcset:
                image_url = srcset.split(',')[0].split(' ')[0]
                # print(i, image_url)
            elif src and src.startswith('data:image/'):
                # print(i, 'data')
                continue

            # url.append(image_url)
            if image_url:
                download_image(image_url, folder_name)
                count += 1

            if count == N_total:
                break

        except StaleElementReferenceException:
            print(f"Элемент устарел, пропускаем.")

    if count == N_total:
        break

    try:
        explore_button = driver.find_element(By.XPATH, '//button[text()="Load more"]')
        # Нажатие на кнопку "Explore"
        explore_button.click()
        print("Кнопка 'Explore' нажата.")
    except:
        print("Кнопка 'Explore' не видна на странице.")

    driver.execute_script("window.scrollBy(0,1000)")

# Закрытие драйвера
driver.quit()

print("Скачивание завершено.")
