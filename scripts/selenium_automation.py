from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    driver = webdriver.Chrome()
    driver.get("http://localhost:8501")

    wait = WebDriverWait(driver, 60)  # Aumente o tempo de espera para 60 segundos

    try:
        # Clicar no botão "Consultar Preços"
        logging.info("Clicando no botão 'Consultar Preços'...")
        consultar_precos_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Consultar preços')]"))
        )
        consultar_precos_button.click()
        time.sleep(3)

        # Navegar até a aba "P9 Diferença de dois veículos"
        logging.info("Navegando até a aba 'P9 Diferença de dois veículos'...")
        aba_tabs = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@role='tablist']//button"))
        )
        # Clicar na quinta aba (índice 4, pois a contagem começa em 0)
        aba_tabs[4].click()
        time.sleep(3)

        # Procurar o dropdown "Selecione a Marca"
        logging.info("Procurando o dropdown 'Selecione a Marca'...")
        marca1_select = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'stSelectbox') and contains(., 'Selecione a Marca')]"))
        )
        logging.info("Dropdown encontrado e clicável.")

        # Rolar a página até o dropdown ficar visível (se necessário)
        actions = ActionChains(driver)
        actions.move_to_element(marca1_select).perform()
        time.sleep(2)

        # Clicar no dropdown "Selecione a Marca"
        marca1_select.click()
        time.sleep(2)

        # Escolher a marca "Volkswagen"
        marca1_option = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//li[contains(., 'Volkswagen')]"))
        )
        marca1_option.click()
        time.sleep(2)

        # ... (restante do script)

    except Exception as e:
        logging.error(f"Erro durante a execução: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()