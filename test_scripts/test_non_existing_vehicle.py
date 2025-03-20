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
        # Open the Streamlit app
        driver.get("http://localhost:8501")

        # Click "Consultar preços" button
        consultar_precos_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Consultar preços')]"))
        )
        consultar_precos_button.click()

        # Wait for UI transition
        time.sleep(3)

        # Click "P7 Comparar duas lojas" tab
        compare_stores_tab = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'P7 Comparar duas lojas')]"))
        )
        compare_stores_tab.click()

        # Wait until the tab content (including selectbox) is loaded
        time.sleep(3)

        elements = driver.find_elements(By.XPATH, "//div[@class='stSelectbox' and contains(normalize-space(), 'Selecione a Marca')]")
        #print("Found buttons:", [e.text for e in elements])
        text_to_find = f"Selecione a Marca\nSelecione uma marca"
        index = [e.text for e in elements].index(text_to_find)
        elements[index].click()

        time.sleep(3)

        options = driver.find_elements(By.XPATH, "//li")
        #print("Available options:", [option.text for option in options])
        choosable_options = []
        for option in options:
            if option.text == "Chevrolet":
                choosable_options.append(option)
        choosen_brand = random.choice(choosable_options)
        choosen_brand.click()

        time.sleep(3)

        elements = driver.find_elements(By.XPATH, "//div[@class='stSelectbox' and contains(normalize-space(), 'Selecione o Modelo')]")
        #print("Found buttons:", [e.text for e in elements])
        text_to_find = f"Selecione o Modelo\nSelecione um modelo"
        index = [e.text for e in elements].index(text_to_find)
        elements[index].click()

        time.sleep(3)

        options = driver.find_elements(By.XPATH, "//li")
        #print("Available options:", [option.text for option in options])
        choosable_options = []
        for option in options:
            if option.text:
                choosable_options.append(option)
        choosen_brand = random.choice(choosable_options)
        choosen_brand.click()

        time.sleep(3)

        elements = driver.find_elements(By.XPATH, "//div[@class='stSelectbox' and contains(normalize-space(), 'Selecione o Veículo')]")
        #print("Found buttons:", [e.text for e in elements])
        text_to_find = f"Selecione o Veículo\nSelecione um veículo"
        index = [e.text for e in elements].index(text_to_find)
        elements[index].click()

        time.sleep(3)

        search_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//input[@role='combobox' and @aria-expanded='true' and not(@disabled) "
                + "and contains(@aria-label, 'Selecione um veículo')]"
            ))
        )
        search_input.send_keys("Typing a non existing vehicle")

        time.sleep(3)

        elements = driver.find_elements(By.XPATH, "//div[@class='stSelectbox' and contains(normalize-space(), 'Selecione o Veículo')]")
        #print("Found buttons:", [e.text for e in elements])
        text_to_find = f"Selecione o Veículo"
        index = [e.text for e in elements].index(text_to_find)
        elements[index].click()

        time.sleep(3)

        options = driver.find_elements(By.XPATH, "//li")
        #print("Available options:", [option.text for option in options])
        choosable_options = []
        for option in options:
            if option.text != "Selecione um veículo" and option.text:
                choosable_options.append(option)
        choosen_brand = random.choice(choosable_options)
        choosen_brand.click()

        time.sleep(3)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
