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
        driver.get("http://localhost:8501")

        consultar_precos_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Consultar preços')]"))
        )
        consultar_precos_button.click()

        time.sleep(3)

        compare_vehicles_tab = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'P8 Comparar dois veículos')]"))
        )
        compare_vehicles_tab.click()

        time.sleep(3)

        elements = driver.find_elements(By.XPATH, "//div[@class='stSelectbox' and contains(normalize-space(), 'Selecione a Marca')]")

        text_to_find = "Selecione a Marca\nSelecione uma marca"
        index = [e.text for e in elements].index(text_to_find)
        elements[index].click()

        time.sleep(1)

        search_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@role='combobox' and @aria-expanded='true' and not(@disabled) and contains(@aria-label, 'Selecione uma marca')]"))
        )

        valid_brand = "Chevrolet"
        search_input.send_keys(valid_brand)

        time.sleep(1)

        options = driver.find_elements(By.XPATH, "//li")
        available_options = [option.text for option in options]
        
        if valid_brand in available_options:
            print(f"Marca válida '{valid_brand}' encontrada!")
        else:
            print(f"Marca válida '{valid_brand}' não foi encontrada na lista!")

        brand_option = [option for option in options if option.text == valid_brand][0]
        brand_option.click()

        time.sleep(1)

        model_elements = driver.find_elements(By.XPATH, "//div[@class='stSelectbox' and contains(normalize-space(), 'Selecione o Modelo')]")
        
        text_to_find_model = "Selecione o Modelo\nSelecione um modelo"
        index_model = [e.text for e in model_elements].index(text_to_find_model)
        model_elements[index_model].click()

        time.sleep(1)

        search_input_model = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@role='combobox' and @aria-expanded='true' and not(@disabled) and contains(@aria-label, 'Selecione um modelo')]"))
        )

        valid_model = "Cruze"
        search_input_model.send_keys(valid_model)

        time.sleep(1)

        options_model = driver.find_elements(By.XPATH, "//li")
        available_model_options = [option.text for option in options_model]

        if valid_model in available_model_options:
            print(f"Modelo válido '{valid_model}' encontrado!")
        else:
            print(f"Modelo válido '{valid_model}' não foi encontrado na lista!")

        model_option = [option for option in options_model if option.text == valid_model][0]
        model_option.click()

        time.sleep(1)

        year_elements = driver.find_elements(By.XPATH, "//div[@class='stSelectbox' and contains(normalize-space(), 'Selecione o Veículo')]")

        text_to_find_year = "Selecione o Veículo\nSelecione um veículo"
        index_year = [e.text for e in year_elements].index(text_to_find_year)
        year_elements[index_year].click()

        time.sleep(1)

        search_input_year = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@role='combobox' and @aria-expanded='true' and not(@disabled) and contains(@aria-label, 'Selecione um veículo')]"))
        )

        invalid_year = "2900"
        search_input_year.send_keys(invalid_year)

        time.sleep(3)

        options_year = driver.find_elements(By.XPATH, "//li")
        available_year_options = [option.text for option in options_year]

        if invalid_year not in available_year_options:
            print(f"Teste passou: Ano inválido '{invalid_year}' não foi encontrado na lista de anos!")
        else:
            print(f"Teste falhou: Ano inválido '{invalid_year}' apareceu na lista de anos!")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
