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

        # Selecionar Marca
        elements = driver.find_elements(By.XPATH, "//div[@class='stSelectbox' and contains(normalize-space(), 'Selecione a Marca')]")
        text_to_find = "Selecione a Marca\nSelecione uma marca"
        index = [e.text for e in elements].index(text_to_find)
        elements[index].click()
        time.sleep(1)

        search_input = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//input[@role='combobox' and @aria-expanded='true' and not(@disabled) and contains(@aria-label, 'Selecione uma marca')]"))
        )

        valid_brand = "Chevrolet"
        search_input.send_keys(valid_brand)
        time.sleep(1)

        options = driver.find_elements(By.XPATH, "//li")
        brand_option = [option for option in options if option.text == valid_brand][0]
        brand_option.click()
        time.sleep(1)

        # Selecionar Modelo
        model_elements = driver.find_elements(By.XPATH, "//div[@class='stSelectbox' and contains(normalize-space(), 'Selecione o Modelo')]")
        text_to_find_model = "Selecione o Modelo\nSelecione um modelo"
        index_model = [e.text for e in model_elements].index(text_to_find_model)
        model_elements[index_model].click()
        time.sleep(1)

        search_input_model = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//input[@role='combobox' and @aria-expanded='true' and not(@disabled) and contains(@aria-label, 'Selecione um modelo')]"))
        )

        valid_model = "Cruze"
        search_input_model.send_keys(valid_model)
        time.sleep(1)

        options_model = driver.find_elements(By.XPATH, "//li")
        model_option = [option for option in options_model if option.text == valid_model][0]
        model_option.click()
        time.sleep(1)

        # Selecionar Ano Modelo
        year_elements = driver.find_elements(By.XPATH, "//div[@class='stSelectbox' and contains(normalize-space(), 'Selecione o Veículo')]")
        text_to_find_year = "Selecione o Veículo\nSelecione um veículo"
        index_year = [e.text for e in year_elements].index(text_to_find_year)
        year_elements[index_year].click()
        time.sleep(1)

        search_input_year = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//input[@role='combobox' and @aria-expanded='true' and not(@disabled) and contains(@aria-label, 'Selecione um veículo')]"))
        )

        valid_year = "2025"
        search_input_year.send_keys(valid_year)
        time.sleep(1)

        options_year = driver.find_elements(By.XPATH, "//li")
        year_option = [option for option in options_year if option.text == valid_year][0]
        year_option.click()
        time.sleep(1)

        search_input_year.send_keys(Keys.TAB)
        time.sleep(1)

        valid_brand_2 = "BYD"
        driver.switch_to.active_element.send_keys(valid_brand_2)
        time.sleep(1)
        driver.switch_to.active_element.send_keys(Keys.ENTER)
        time.sleep(1)
        
        driver.switch_to.active_element.send_keys(Keys. TAB)
        time.sleep(1)

        valid_model_2 = "3001"
        driver.switch_to.active_element.send_keys(valid_model_2)
        time.sleep(1)
        driver.switch_to.active_element.send_keys(Keys.ENTER)
        time.sleep(1)

        driver.switch_to.active_element.send_keys(Keys. TAB)
        time.sleep(1)

        valid_year_2 = "1900"
        driver.switch_to.active_element.send_keys(valid_year_2)
        time.sleep(1)
        driver.switch_to.active_element.send_keys(Keys.ENTER)
        time.sleep(1)

        driver.switch_to.active_element.send_keys(Keys. TAB)
        time.sleep(1)

        valid_month_1 = "January"
        driver.switch_to.active_element.send_keys(valid_month_1)
        time.sleep(1)
        driver.switch_to.active_element.send_keys(Keys.ENTER)
        time.sleep(1)

        driver.switch_to.active_element.send_keys(Keys. TAB)
        time.sleep(1)

        invalid_year_1 = "3000"
        driver.switch_to.active_element.send_keys(invalid_year_1)
        time.sleep(3)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
