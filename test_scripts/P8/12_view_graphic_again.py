from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import time

def main():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("http://localhost:8501")

        google_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Entre com google')]"))
        )
        google_button.click()

        time.sleep(3)

        email_input = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='email']"))
        )
        email_input.send_keys("usuariocomparador@gmail.com")

        next_button = driver.find_element(By.XPATH, "//span[contains(., 'Próxima')]")
        next_button.click()

        time.sleep(3)

        password_input = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
        )
        password_input.send_keys("compareruser")  

        next_button = driver.find_element(By.XPATH, "//span[contains(., 'Próxima')]")
        next_button.click()

        time.sleep(3)

        next_button = driver.find_element(By.XPATH, "//span[contains(., 'Continue')]")
        next_button.click()

        time.sleep(3)

        consultar_precos_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Consultar preços')]"))
        )
        consultar_precos_button.click()

        time.sleep(3)

        compare_vehicles_tab = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Minhas consultas')]"))
        )
        compare_vehicles_tab.click()

        time.sleep(8)

        driver.switch_to.active_element.send_keys(Keys. TAB)
        driver.switch_to.active_element.send_keys(Keys. TAB)
        driver.switch_to.active_element.send_keys(Keys. TAB)
        driver.switch_to.active_element.send_keys(Keys. ENTER)
        time.sleep(2)

        driver.switch_to.active_element.send_keys(Keys. TAB)
        driver.switch_to.active_element.send_keys(Keys. TAB)
        driver.switch_to.active_element.send_keys(Keys. ENTER)
        time.sleep(2)
        driver.switch_to.active_element.send_keys(Keys. PAGE_DOWN)
        time.sleep(5)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()