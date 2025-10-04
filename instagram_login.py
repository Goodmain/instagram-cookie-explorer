import os
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def get_instagram_cookies():
    """
    Logs into Instagram and saves session cookies.
    """
    username = os.environ.get("INSTAGRAM_USERNAME")
    password = os.environ.get("INSTAGRAM_PASSWORD")

    if not username or not password:
        print("Please set the INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD environment variables.")
        return

    chrome_options = Options()
    # The browser needs to run in non-headless mode to be interactive for 2FA
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")


    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get("https://www.instagram.com/accounts/login/")

        # Wait for the username field to be present
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        username_field.send_keys(username)

        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys(password)

        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()

        # Wait for 2FA input field
        try:
            two_fa_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "verificationCode"))
            )
            two_fa_code = input("Enter the 2FA code: ")
            two_fa_field.send_keys(two_fa_code)

            confirm_button = driver.find_element(By.XPATH, "//button[contains(text(),'Confirm')]")
            confirm_button.click()

        except TimeoutException:
            # This is not an error, it just means 2FA was not requested
            print("2FA not requested, proceeding.")
            pass


        # Wait for login to complete by checking for the presence of the profile icon
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='button'] img[data-testid='user-avatar']"))
        )

        print("Login successful!")

        # Get cookies
        cookies = driver.get_cookies()

        # Save cookies to a file in the mounted volume
        output_path = "/app/output/instagram_cookies.json"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(cookies, f)

        print(f"Cookies saved to {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")
        driver.save_screenshot("error_screenshot.png")

    finally:
        driver.quit()

if __name__ == "__main__":
    get_instagram_cookies()