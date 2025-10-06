import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Configuration ---
INSTAGRAM_URL = "https://www.instagram.com"
COOKIES_FILE_PATH = "/app/output/instagram_cookies.txt" # Path inside the Docker container

# --- Get Credentials from Environment Variables ---
# It's safer to pass credentials this way than hardcoding them.
IG_USERNAME = os.getenv("IG_USERNAME")
IG_PASSWORD = os.getenv("IG_PASSWORD")

if not IG_USERNAME or not IG_PASSWORD:
    raise ValueError("Error: IG_USERNAME and IG_PASSWORD environment variables must be set.")

# --- Setup Selenium WebDriver ---
print("🚀 Starting Selenium WebDriver...")
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in the background without a GUI
chrome_options.add_argument("--no-sandbox") # Required for running as root in Docker
chrome_options.add_argument("--disable-dev-shm-usage") # Overcome limited resource problems
chrome_options.add_argument("--window-size=1920,1080") # Set a reasonable window size

# The webdriver manager is handled by the Dockerfile setup
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 20) # Set a generous wait time

try:
    print(f"Navigating to {INSTAGRAM_URL}...")
    driver.get(INSTAGRAM_URL)

    # --- Login Process ---
    # 1. Wait for username field and enter username
    username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    username_field.send_keys(IG_USERNAME)
    print("✅ Username entered.")

    # 2. Find and enter password
    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys(IG_PASSWORD)
    print("✅ Password entered.")

    # 3. Click login button
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()
    print("🖱️ Login button clicked. Waiting for next page...")

    # --- 2FA (Two-Factor Authentication) Handling ---
    try:
        # Wait for the 2FA input field to appear
        two_fa_field = wait.until(EC.presence_of_element_located((By.NAME, "email")))
        print("\n🔒 2FA code required.")
        
        # Prompt user to enter the 2FA code in the terminal
        two_fa_code = input("Please enter the 6-digit code from your authenticator app: ")
        
        two_fa_field.send_keys(two_fa_code)
        
        # Click confirm button
        confirm_button = driver.find_element(By.XPATH, "//span[text()='Continue']")
        confirm_button.click()
        print("✅ 2FA code submitted.")

    except Exception:
        print("🤔 2FA prompt not detected. Either 2FA is off or login failed.")

    # --- Verify Login and Save Cookies ---
    # We verify login by looking for an element that only appears on the home feed,
    # like the "Not Now" button for "Turn on Notifications".
    print("Verifying login success...")
    wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Home']")))
    
    print("\n🎉 Login successful!")

    # Get cookies from the current session
    cookies = driver.get_cookies()

    # Save cookies to the specified file path
    os.makedirs(os.path.dirname(COOKIES_FILE_PATH), exist_ok=True)
    with open(COOKIES_FILE_PATH, 'w') as f:
        # Write the standard Netscape header
        f.write("# Netscape HTTP Cookie File\n")
        f.write("# http://www.netscape.com/newsref/std/cookie_spec.html\n")

        # Convert and write each cookie
        for cookie in cookies:
            # The flag is TRUE if the cookie is for subdomains, which is the opposite of Selenium's hostOnly flag.
            flag = str(not cookie.get('hostOnly', True)).upper()
            
            # Expiry needs to be an integer. If 'expiry' is not present, use 0.
            expiration = str(int(cookie.get('expiry', 0)))

            # Write the tab-separated line
            f.write(
                f"{cookie.get('domain', '')}\t"
                f"{flag}\t"
                f"{cookie.get('path', '')}\t"
                f"{str(cookie.get('secure', False)).upper()}\t"
                f"{expiration}\t"
                f"{cookie.get('name', '')}\t"
                f"{cookie.get('value', '')}\n"
            )

    print(f"🍪 Cookies have been successfully exported in Netscape format to {COOKIES_FILE_PATH}")
    print("You can find the 'instagram_cookies.txt' file in the 'output' folder on your local machine.")

except Exception as e:
    print(f"\n❌ An error occurred: {e}")
    # Optional: Save a screenshot for debugging
    driver.save_screenshot("/app/output/error_screenshot.png")
    with open("/app/output/page_source.html", "w", encoding='utf-8') as f:
        page_html = driver.page_source
        f.write(page_html)
    print("📸 A screenshot has been saved to the 'output' folder for debugging.")

finally:
    # --- Cleanup ---
    print(" shutting down WebDriver.")
    driver.quit()