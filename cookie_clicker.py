from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)


driver = webdriver.Chrome(options=chrome_options)
# driver.get("https://en.wikipedia.org/wiki/Main_Page")
driver.get("https://orteil.dashnet.org/cookieclicker/")

time.sleep(5)
language = driver.find_element(By.ID, 'langSelect-EN')
language.click()

duration_min = 5  # Run the loop for 1 minute
interval = 5
last_action_time = time.time()
end_time = time.time() + duration_min * 60

cookie = driver.find_element(By.ID, 'bigCookie')
cursor_button = driver.find_element(By.XPATH, '//*[@id="product0"]')
grandma_button = driver.find_element(By.XPATH, '//*[@id="product1"]')
farm_button = driver.find_element(By.XPATH, '//*[@id="product2"]')
mine_button = driver.find_element(By.XPATH, '//*[@id="product3"]')

while time.time() < end_time:
    cookie.click()
    if time.time() - last_action_time >= 5:
        cookies = int(driver.find_element(By.ID, 'cookies').text.split()[0])

        # Helper function to safely extract price
        def get_price(product_id):
            price_text = driver.find_element(By.ID, product_id).text.replace(',', '').strip()
            return int(price_text) if price_text else float('inf')  # inf means "too expensive"


        cursor = get_price('productPrice0')
        grandma = get_price('productPrice1')
        farm = get_price('productPrice2')
        mine = get_price('productPrice3')

        # Create a list of affordable items and their corresponding buttons
        affordable_items = [
            (cursor, cursor_button),
            (grandma, grandma_button),
            (farm, farm_button),
            (mine, mine_button)
        ]
        affordable_items = [(price, button) for price, button in affordable_items if price <= cookies]
        if affordable_items:
            # Find the most expensive affordable item
            most_expensive = max(affordable_items, key=lambda item: item[0])
            # Click the button for the most expensive affordable item
            most_expensive[1].click()
            # Update the last action time
            last_action_time = time.time()


print(f"Loop finishes after {duration_min} minutes")
print('Final cookies: ')
print(int(driver.find_element(By.ID, 'cookies').text.split()[0]))