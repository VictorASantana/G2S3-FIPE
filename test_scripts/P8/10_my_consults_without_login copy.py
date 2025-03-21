from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def main():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("http://localhost:8501")

        consultar_precos_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Consultar preços')]"))
        )
        consultar_precos_button.click()

        time.sleep(3)

        compare_vehicles_tab = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Minhas consultas')]"))
        )
        compare_vehicles_tab.click()

        time.sleep(4)
        
    finally:
        driver.quit()

if __name__ == "__main__":
    main()