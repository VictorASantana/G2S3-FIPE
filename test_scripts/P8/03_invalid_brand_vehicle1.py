from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

def main():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    try:
        # Abrir o Streamlit app
        driver.get("http://localhost:8501")

        # Clicar no botão "Consultar preços"
        consultar_precos_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Consultar preços')]"))
        )
        consultar_precos_button.click()

        # Esperar a transição da UI
        time.sleep(3)

        # Clicar na aba "P8 Comparar dois veículos"
        compare_vehicles_tab = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'P8 Comparar dois veículos')]"))
        )
        compare_vehicles_tab.click()

        # Esperar carregar a aba
        time.sleep(3)

        # Selecionar a Marca do Veículo 1
        elements = driver.find_elements(By.XPATH, "//div[@class='stSelectbox' and contains(normalize-space(), 'Selecione a Marca')]")
        
        # Buscar o índice do select correto
        text_to_find = "Selecione a Marca\nSelecione uma marca"
        index = [e.text for e in elements].index(text_to_find)
        elements[index].click()

        time.sleep(1)

        # Localizar a barra de pesquisa da marca
        search_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@role='combobox' and @aria-expanded='true' and not(@disabled) and contains(@aria-label, 'Selecione uma marca')]"))
        )

        # Digitar uma marca inválida
        invalid_brand = "Marca Inexistente 123"
        search_input.send_keys(invalid_brand)

        time.sleep(3)

        # Verificar se a lista de opções contém a marca digitada
        options = driver.find_elements(By.XPATH, "//li")
        available_options = [option.text for option in options]

        if invalid_brand not in available_options:
            print("Teste passou: Marca inválida não foi encontrada na lista!")
        else:
            print("Teste falhou: Marca inválida apareceu na lista!")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
