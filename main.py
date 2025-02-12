from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
import urllib.request
import time
from chromedriver_py import binary_path
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# to run Chrome in headless mode
options = Options()
options.add_argument("--headless")
#options.add_argument("--no-sandbox")
#options.add_argument("--disable-dev-shm-usage")

query = 'laptop'

svc = webdriver.ChromeService(executable_path=binary_path)
driver = webdriver.Chrome(
    service=svc
)

driver.maximize_window()

# the URL of the target page
url = f"https://unsplash.com/s/photos/{query}?license=free"
# visit the target page in the controlled browser
driver.get(url)

# select the node images on the page
# image_html_nodes = driver.find_elements(By.CSS_SELECTOR, "[data-test=\"photo-grid-masonry-img\"]")
# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


# images[0].get_attribute('src')
# where to store the scraped image url

count = 0
images = driver.find_elements(By.TAG_NAME, 'img')
# images  = driver.execute_script("return window.performance.getEntriesByType('resource');")
count = count + len(images)
last_height = driver.execute_script("return document.body.scrollHeight")
# last_height = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")

try:
    # explore_button = WebDriverWait(driver, 1).until(
    #    EC.visibility_of_element_located((By.CLASS_NAME, 'ZGh7S kx6eK x_EXo R6ToQ QcIGU l0vpf a_AEd ncszm MCje9 daPLj R6ToQ'))
    # )
    # explore_button=driver.find_element(By.CLASS_NAME, 'ZGh7S kx6eK x_EXo R6ToQ QcIGU l0vpf a_AEd ncszm MCje9 daPLj R6ToQ')
    explore_button = driver.find_element(By.XPATH, '//button[text()="Load more"]')
    # Нажатие на кнопку "Explore"
    explore_button.click()
    print("Кнопка 'Explore' нажата.")
except:
    print("Кнопка 'Explore' не видна на странице.")

while True:

    driver.execute_script("window.scrollBy(0,1000)")
    #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(1)

    #driver.maximize_window()

    #images = driver.find_elements(By.TAG_NAME, 'img')
    #count = count + len(images)
    #print(count)
    new_height = driver.execute_script("return document.body.scrollHeight")

    #if new_height == last_height:
    #    break

    #last_height = new_height
    images = driver.find_elements(By.TAG_NAME, 'img')
    count = count + len(images)
    print(count)

print(count)
driver.quit()
# image_urls = []
#
# image_html_nodes = images
# # extract the URLs from each image
# for image_html_node in image_html_nodes:
#     try:
#         # use the URL in the "src" as the default behavior
#         image_url = image_html_node.get_attribute("src")
#
#         # extract the URL of the largest image from "srcset",
#         # if this attribute exists
#         srcset = image_html_node.get_attribute("srcset")
#         if srcset is not None:
#             # get the last element from the "srcset" value
#             srcset_last_element = srcset.split(", ")[-1]
#             # get the first element of the value,
#             # which is the image URL
#             image_url = srcset_last_element.split(" ")[0]
#
#         # add the image URL to the list
#         image_urls.append(image_url)
#     except StaleElementReferenceException as e:
#         continue
#
# # to keep track of the images saved to disk
# image_name_counter = 1
#
# # download each image and add it
# # to the "/images" local folder
# for image_url in image_urls:
#     print(f"downloading image no. {image_name_counter} ...")
#
#     file_name = f"./images/{image_name_counter}.jpg"
#     # download the image
#     urllib.request.urlretrieve(image_url, file_name)
#
#     print(f"images downloaded successfully to \"{file_name}\"\n")
#
#     # increment the image counter
#     image_name_counter += 1
#
# # close the browser and free up its resources
# driver.quit()
#
# pass
