import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Set up the Chrome WebDriver with headless option
options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

# Set up settings variables
FOLDER = "data/"
FILE_NAME="restaurants.csv"
NUM_OF_PAGES = 4

cities = ["torino", "milano", "genova", "bologna", "venezia", "verona"]
restaurants_data = []


def get_existing_emails():
    try:
        with open(FOLDER + FILE_NAME) as f:
            return [line.split(';')[1].strip() for line in f]
    except:
        return []


existing_emails = get_existing_emails()


def get_text_from_element(restaurant_element):
    try:
        return restaurant_element.text
    except:
        return ''


def iterate_website_links_for_page():
    website_links = WebDriverWait(driver, 1000).until(
        EC.presence_of_all_elements_located((By.LINK_TEXT, "Website")))
    restaurants_names = WebDriverWait(driver, 1000).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".rllt__details > div:nth-child(1) > span")))

    for index, wlink in enumerate(website_links):
        restaurant_name = get_text_from_element(restaurants_names[index])
        print("Restaurant: ", restaurant_name)
        try:
            driver.execute_script("arguments[0].scrollIntoView();", wlink)
            WebDriverWait(driver, 5000).until(EC.element_to_be_clickable(wlink)).click()
        except:
            print('Error while clicking on Website link')
            continue

        # Get the page source and search for the email
        page_source = driver.page_source
        email = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', page_source)

        restaurant = {
            'name': restaurant_name,
            'email': email.group() if email else ''
        }

        if restaurant['email'] and restaurant['email'] not in existing_emails:
            restaurants_data.append(restaurant)
            existing_emails.append(restaurant['email'])

        # Navigate back to the list of restaurants
        driver.back()


def iterate_pages_by_city(city):
    global restaurants_data
    # Start google search
    driver.get(f"https://www.google.com/search?q=ristoranti+{city}")
    # Click on the "More places" button
    WebDriverWait(driver, 1000).until(EC.element_to_be_clickable((By.LINK_TEXT, "More places"))).click()
    for i in range(0, NUM_OF_PAGES):
        print("Page: ", i + 1)

        iterate_website_links_for_page()

        print("Writing %d restaurants to file for page %d" % (len(restaurants_data), i + 1))
        with open(FOLDER + FILE_NAME, 'a') as f:
            for r in restaurants_data:
                f.write("%s;%s;%s\n" % (city, r['name'], r['email']))

        # Clear restaurants data for the next page
        restaurants_data = []

        try:
            WebDriverWait(driver, 1000).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="pnnext"]/g-right-button'))).click()
        except:
            print('Error while clicking on next page button')
            WebDriverWait(driver, 1000).until(EC.element_to_be_clickable((By.LINK_TEXT, "More places"))).click()
            continue


for c in cities:
    iterate_pages_by_city(c)

driver.quit()
