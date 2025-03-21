from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import random

from datetime import datetime

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
            if option.text == "Onix":
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

        options = driver.find_elements(By.XPATH, "//li")
        #print("Available options:", [option.text for option in options])
        choosable_options = []
        for option in options:
            if option.text == "2021":
                choosable_options.append(option)
        choosen_brand = random.choice(choosable_options)
        choosen_brand.click()

        time.sleep(3)

        elements = driver.find_elements(By.XPATH, "//div[@class='stSelectbox' and contains(normalize-space(), 'Selecione uma loja')]")
        text_to_find = f"Selecione uma loja\nSelecione uma loja"
        elements[0].click()

        time.sleep(3)
        options = driver.find_elements(By.XPATH, "//li")
        # print("Available options:", [option.text for option in options])
        choosable_options = []
        for option in options:
            if option.text == "AutoCar SP":
                choosable_options.append(option)
        choosen_store = random.choice(choosable_options)
        choosen_store.click()

        time.sleep(3)

        elements[1].click()

        time.sleep(3)

        options = driver.find_elements(By.XPATH, "//li")
        # print("Available options:", [option.text for option in options])
        choosable_options = []
        for option in options:
            if option.text == "Veículos RJ":
                choosable_options.append(option)
        choosen_store = random.choice(choosable_options)
        choosen_store.click()

        time.sleep(3)

        elements = driver.find_elements(By.XPATH, "//div[@class='stDateInput' and contains(normalize-space(), 'Data inicial')]")
        #print("Found buttons:", [e.text for e in elements])
        text_to_find = f"Data inicial"
        index = [e.text for e in elements].index(text_to_find)
        elements[index].click()

        time.sleep(3)

        date_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@data-testid='stDateInputField' and not(@disabled)]"))
        )
        date_input.click()
        date_input.send_keys(Keys.CONTROL, "a")
        date_input.send_keys(Keys.DELETE)
        date_input.send_keys("2065/01/01")
        date_input.send_keys(Keys.ENTER)

        time.sleep(5)

        elements = driver.find_elements(By.XPATH, "//div[@class='stDateInput' and contains(normalize-space(), 'Data inicial')]")
        #print("Found buttons:", [e.text for e in elements])
        text_to_find = f"Data inicial"
        index = [e.text for e in elements].index(text_to_find)
        elements[index].click()

        time.sleep(3)
        
        for _ in range(3):
            # Go back one year
            mont_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(@aria-label, 'Previous month')]")
                )
            )
            mont_button.click()
            time.sleep(0.5)

        day_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@role='gridcell' and contains(@aria-label, 'December 18th 2024')]")
            )
        )
        day_button.click()

        time.sleep(3)

# Open the "Data final" container
        data_final_container = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//div[@class='stDateInput' and contains(., 'Data final')])[1]"))
        )
        data_final_container.click()

        time.sleep(3)

        # Locate the input within the Data final container by scoping the search within that container:
        date_input = WebDriverWait(data_final_container, 10).until(
            EC.visibility_of_element_located((By.XPATH, ".//input[@data-testid='stDateInputField' and not(@disabled)]"))
        )
        date_input.click()
        date_input.send_keys(Keys.CONTROL, "a")
        date_input.send_keys(Keys.DELETE)
        date_input.send_keys("2065/01/01")
        time.sleep(1)
        date_input.send_keys(Keys.ENTER)

        time.sleep(5)

        # Re-find the Data final container again before opening the calendar
        data_final_container = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//div[@class='stDateInput' and contains(., 'Data final')])[1]"))
        )
        data_final_container.click()

        time.sleep(3)

        # Now click on the day from the calendar (global search might work if the correct calendar is visible)
        day_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@role='gridcell' and contains(@aria-label, 'March 19th 2025')]")
            )
        )
        day_button.click()

        time.sleep(3)

        all_buttons = driver.find_elements(By.TAG_NAME, "button")

        choosable_options = []
        for option in all_buttons:
            if option.text == "Comparar lojas":
                choosable_options.append(option)
        choosen_store = random.choice(choosable_options)
        choosen_store.click()

        time.sleep(5)
        
        body = driver.find_element(By.TAG_NAME, 'body')
        body.send_keys(Keys.PAGE_DOWN)
        
        time.sleep(5)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
