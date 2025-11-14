from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_saucedemo_purchase_flow():

    options = Options()
    options.add_argument("--window-size=1920,1080")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(3)
    wait = WebDriverWait(driver, 10)

    try:

        driver.get("https://www.saucedemo.com")
        time.sleep(1)
        
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        time.sleep(0.5)
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        time.sleep(0.5)
        
        login_btn = driver.find_element(By.ID, "login-button")
        driver.execute_script("arguments[0].click();", login_btn)

        time.sleep(2)
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "inventory_list")))

        items = driver.find_elements(By.CLASS_NAME, "inventory_item")
        first_item = items[0]
        product_name = first_item.find_element(By.CLASS_NAME, "inventory_item_name").text
        
        print(f"Adding to cart: {product_name}")
        
        add_btn = first_item.find_element(By.TAG_NAME, "button")
        driver.execute_script("arguments[0].click();", add_btn)
        time.sleep(1)

        cart_link = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        driver.execute_script("arguments[0].click();", cart_link)
        time.sleep(2)
        
        cart_product_name = driver.find_element(By.CLASS_NAME, "inventory_item_name").text
        
        if product_name == cart_product_name:
            print(f"Cart verification passed: {cart_product_name}")
        else:
            raise AssertionError(f"Expected '{product_name}', but got '{cart_product_name}'")
        
        time.sleep(1)

        menu_btn = driver.find_element(By.ID, "react-burger-menu-btn")
        driver.execute_script("arguments[0].click();", menu_btn)
        time.sleep(1)
        
        wait.until(EC.presence_of_element_located((By.ID, "logout_sidebar_link")))
        logout_btn = driver.find_element(By.ID, "logout_sidebar_link")
        driver.execute_script("arguments[0].click();", logout_btn)
        time.sleep(1)

        print("Test completed successfully")

    except Exception as e:
        print(f"Test failed: {str(e)}")
        raise
    finally:
        driver.quit()


if __name__ == "__main__":
    test_saucedemo_purchase_flow()
