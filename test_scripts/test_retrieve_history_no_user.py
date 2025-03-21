from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def main():
    driver = webdriver.Chrome()

    try:
        # Open the Streamlit app
        driver.get("http://localhost:8501")

        time.sleep(5)

        # Wait for the "Consultar preços" button and click it
        wait = WebDriverWait(driver, 10)
        consultar_precos_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Consultar preços')]"))
        )
        consultar_precos_button.click()

        # Wait to observe changes (adjust as needed)
        time.sleep(3)

        # Locate and click the "Minhas consultas" tab
        minhas_consultas_tab = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Minhas consultas')]"))
        )
        minhas_consultas_tab.click()

        # Wait to observe the tab content (adjust as needed)
        time.sleep(5)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
