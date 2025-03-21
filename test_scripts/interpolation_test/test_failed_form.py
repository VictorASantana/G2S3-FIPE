import time
import random
import unittest
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

STREAMLIT_SCRIPT_PATH = "main.py"

def start_streamlit():
  return subprocess.Popen(["streamlit", "run", STREAMLIT_SCRIPT_PATH])

class InterpolationTabTest(unittest.TestCase):
  def setUp(self):
    self.driver = webdriver.Chrome()
    self.driver.get("http://localhost:8501")
    self.process = start_streamlit()

  #Non existing brand
  def test_non_existing_brand(self):
    driver = self.driver
    wait = WebDriverWait(driver, 10)

    price_search_button = wait.until(
      EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Consultar preços')]"))
    )

    price_search_button.click()

    time.sleep(3)

    future_prices_tab = wait.until(
      EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'P10 Preços futuros')]"))
    )

    future_prices_tab.click()

    elements = driver.find_elements(By.XPATH, "//div[@class='stSelectbox' and contains(normalize-space(), 'Selecione a Marca')]")
    text_to_find = f"Selecione a Marca\nSelecione uma marca"
    index = [e.text for e in elements].index(text_to_find)
    elements[index].click()

    time.sleep(3)
    
    search_input = wait.until(
        EC.visibility_of_element_located((
            By.XPATH,
            "//input[@role='combobox' and @aria-expanded='true' and not(@disabled) "
            + "and contains(@aria-label, 'Selecione uma marca')]"
        ))
    )
    search_input.send_keys("Typing a non existing brand")

    time.sleep(3)

    next_input = wait.until(
       EC.invisibility_of_element_located((
          By.XPATH, 
          "//input[@role='combobox' and @aria-expanded='true' and (@disabled) "
          + "and contains(@aria-label, 'Selecione um modelo')]"
       ))
    )

    self.assertTrue(next_input, "Elemento não está desabilitado")

    time.sleep(3)

  #Non existing model
  def test_non_existing_model(self):
    driver = self.driver
    wait = WebDriverWait(driver, 10)

    price_search_button = wait.until(
      EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Consultar preços')]"))
    )

    price_search_button.click()

    time.sleep(3)

    future_prices_tab = wait.until(
      EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'P10 Preços futuros')]"))
    )

    future_prices_tab.click()

    elements = driver.find_elements(By.XPATH, "//div[@class='stSelectbox' and contains(normalize-space(), 'Selecione a Marca')]")
    text_to_find = f"Selecione a Marca\nSelecione uma marca"
    index = [e.text for e in elements].index(text_to_find)
    elements[index].click()

    time.sleep(3)
    
    options = driver.find_elements(By.XPATH, "//li")
    choosable_options = []
    for option in options:
        if option.text == "Honda":
            choosable_options.append(option)
    choosen_brand = random.choice(choosable_options)
    choosen_brand.click()

    time.sleep(3)

    elements = driver.find_elements(By.XPATH, "//div[@class='stSelectbox' and contains(normalize-space(), 'Selecione o Modelo')]")
    text_to_find = f"Selecione o Modelo\nSelecione um modelo"
    index = [e.text for e in elements].index(text_to_find)
    elements[index].click()

    time.sleep(3)

    search_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((
            By.XPATH,
            "//input[@role='combobox' and @aria-expanded='true' and not(@disabled) "
            + "and contains(@aria-label, 'Selecione um modelo')]"
        ))
    )
    search_input.send_keys("Typing a non existing model")

    time.sleep(3)

    next_input = wait.until(
       EC.invisibility_of_element_located((
          By.XPATH, 
          "//input[@role='combobox' and @aria-expanded='true' and (@disabled) "
          + "and contains(@aria-label, 'Selecione um veículo')]"
       ))
    )

    self.assertTrue(next_input, "Elemento não está desabilitado")

    time.sleep(3)

  #Non existing vehicle
  def test_non_existing_vehicle(self):
    driver = self.driver
    wait = WebDriverWait(driver, 10)

    price_search_button = wait.until(
      EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Consultar preços')]"))
    )

    price_search_button.click()

    time.sleep(3)

    future_prices_tab = wait.until(
      EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'P10 Preços futuros')]"))
    )

    future_prices_tab.click()

    elements = driver.find_elements(By.XPATH, "//div[@class='stSelectbox' and contains(normalize-space(), 'Selecione a Marca')]")
    text_to_find = f"Selecione a Marca\nSelecione uma marca"
    index = [e.text for e in elements].index(text_to_find)
    elements[index].click()

    time.sleep(3)
    
    options = driver.find_elements(By.XPATH, "//li")
    choosable_options = []
    for option in options:
        if option.text == "Honda":
            choosable_options.append(option)
    choosen_brand = random.choice(choosable_options)
    choosen_brand.click()

    time.sleep(3)

    elements = driver.find_elements(By.XPATH, "//div[@class='stSelectbox' and contains(normalize-space(), 'Selecione o Modelo')]")
    text_to_find = f"Selecione o Modelo\nSelecione um modelo"
    index = [e.text for e in elements].index(text_to_find)
    elements[index].click()

    time.sleep(3)

    options = driver.find_elements(By.XPATH, "//li")
    #print("Available options:", [option.text for option in options])
    choosable_options = []
    for option in options:
        if option.text == 'CR-V':
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

    search_button = wait.until(
       EC.invisibility_of_element_located((
          By.XPATH, 
          "//button[contains(., 'Pesquisar preço')]"
       ))
    )

    self.assertTrue(search_button, "Elemento não está desabilitado")

    time.sleep(3)
    
  def tear_down(self):
    self.driver.quit()
    self.process.terminate()
  
if __name__ == "__main__":
  unittest.main()
