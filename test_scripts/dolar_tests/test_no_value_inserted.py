from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import random


def wait_for_clickable(driver, xpath):
    return WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )

def wait_for_dropdown_options(driver):
    return WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//ul[@data-baseweb='menu']"))
    )

def select_option(driver, label_text, option_text):
    elements = driver.find_elements(By.XPATH, "//div[@class='stSelectbox']")
    for el in elements:
        if label_text in el.text:
            el.click()
            break

    time.sleep(1)

    options = driver.find_elements(By.XPATH, "//li")
    for opt in options:
        if opt.text.strip() == option_text.strip():
            opt.click()
            break

    time.sleep(1)


def click_button_by_text(driver, text):
    buttons = driver.find_elements(By.TAG_NAME, "button")
    for btn in buttons:
        if text.strip().lower() in btn.text.strip().lower():
            driver.execute_script("arguments[0].scrollIntoView(true);", btn)
            driver.execute_script("arguments[0].click();", btn)
            time.sleep(1)
            return
    raise Exception(f"Botão com texto '{text}' não encontrado.")

# === FLUXO PRINCIPAL === #

def main():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("http://localhost:8501")
        wait_for_clickable(driver, "//button[contains(., 'Consultar preços')]").click()
        time.sleep(3)

        wait_for_clickable(driver, "//button[contains(., 'P6 Comparação com dólar')]").click()
        time.sleep(3)
        select_option(driver, "Selecione a Marca", "Chevrolet")
        select_option(driver, "Selecione o Modelo", "Onix")
        select_option(driver, "Selecione o Veículo", "2021")

        # select_option(driver, "Mês Inicial", 'January')
        select_option(driver, "Ano Inicial", '2008')
        # select_option(driver, "Mês Final", 'December')
        select_option(driver, "Ano Final", '2009')

        click_button_by_text(driver, "Comparar veículo com Dólar")

        print("Clique no botão de comparar realizado com sucesso.")

        time.sleep(5)
    
    finally:
        print("Encerrando navegador.")
        driver.quit()

if __name__ == "__main__":
    main()
