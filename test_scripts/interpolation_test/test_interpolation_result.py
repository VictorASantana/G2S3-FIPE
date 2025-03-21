import os
import sys
import time
import random
import unittest
import subprocess
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from utils.exponential import exponential_interpolation

STREAMLIT_SCRIPT_PATH = "main.py"

def start_streamlit():
  return subprocess.Popen(["streamlit", "run", STREAMLIT_SCRIPT_PATH])

class InterpolationTabTest(unittest.TestCase):
  def setUp(self):
    self.driver = webdriver.Chrome()
    self.driver.get("http://localhost:8501")
    self.process = start_streamlit()

  #Testing vehicle with no info
  def test_no_info_vehicle(self):
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
    #print("Found buttons:", [e.text for e in elements])
    text_to_find = f"Selecione a Marca\nSelecione uma marca"
    index = [e.text for e in elements].index(text_to_find)
    elements[index].click()
    
    time.sleep(3)

    options = driver.find_elements(By.XPATH, "//li")
    choosable_options = []
    for option in options:
        if option.text == "Renault":
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
    choosable_options = []
    for option in options:
      if option.text == "Kwid":
        choosable_options.append(option)
    choosen_model = random.choice(choosable_options)
    choosen_model.click()

    time.sleep(3)

    elements = driver.find_elements(By.XPATH, "//div[@class='stSelectbox' and contains(normalize-space(), 'Selecione o Veículo')]")
    text_to_find = f"Selecione o Veículo\nSelecione um veículo"
    index = [e.text for e in elements].index(text_to_find)
    elements[index].click()

    time.sleep(3)

    options = driver.find_elements(By.XPATH, "//li")
    choosable_options = []
    for option in options:
        if option.text == "2020":
            choosable_options.append(option)
    choosen_brand = random.choice(choosable_options)
    choosen_brand.click()

    time.sleep(5)

    all_buttons = driver.find_elements(By.TAG_NAME, "button")
    choosable_options = []
    for option in all_buttons:
        if option.text == "Pesquisar preço":
            choosable_options.append(option)
    choosen_store = random.choice(choosable_options)
    choosen_store.click()

    time.sleep(3)

    body = driver.find_element(By.TAG_NAME, 'body')
    body.send_keys(Keys.PAGE_DOWN)

    time.sleep(3)

    self.assertIn("O carro selecionado não tem dados suficientes", driver.page_source, "Projeções carregadas")

  #Testing interpolation function
  def test_interpolation_result(self):
    formatted_data = [
      {
         'date': datetime(2024, 1, 1),
         'value': 100
      },
      {
         'date': datetime(2024, 2, 1),
         'value': 200
      },
      {
         'date': datetime(2024, 3, 1),
         'value': 300
      }
    ]

    result = exponential_interpolation(formatted_data, None, None)

    self.assertAlmostEqual(round(float(result['a'].item()), 2), 104.91)
    self.assertAlmostEqual(round(float(result['b'].item()), 2), 0.55)
  
  def tear_down(self):
    self.driver.quit()
    self.process.terminate()
  
if __name__ == "__main__":
  unittest.main()
