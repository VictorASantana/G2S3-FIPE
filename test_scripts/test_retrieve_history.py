from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def main():
    driver = webdriver.Chrome()
    driver.get("http://localhost:8501")

    wait = WebDriverWait(driver, 10)

    try:
        # Click "Entrar com Google" button
        google_login_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'google')]"))
        )
        google_login_button.click()

        # # Wait for new window (Google Login popup)
        # time.sleep(2)  # Small delay to allow window switch

        # # Switch to the Google login window
        # main_window = driver.current_window_handle
        # for handle in driver.window_handles:
        #     if handle != main_window:
        #         driver.switch_to.window(handle)
        #         break  # Found the Google login window

        # # Wait for email input field
        # email_input = wait.until(
        #     EC.presence_of_element_located((By.XPATH, "//input[@type='email']"))
        # )
        # email_input.send_keys("luccagamballi@gmail.com")  # Replace with your email

        # # Click "Next" button
        # next_button = driver.find_element(By.XPATH, "//span[contains(., 'Next')]")
        # next_button.click()

        # # (Optional) Wait and handle password input in a similar way...

        # time.sleep(5)  # Observe results

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
