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

  #Tab loading test
  def test_page_load(self):
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

    self.assertIn("Consultar Interpolação Exponencial:", driver.page_source, "Página não contém o texto esperado")
    
  # Testing table and graphic generations
  def test_entire_flow(self):
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
    #print("Available options:", [option.text for option in options])
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
    choosable_options = []
    for option in options:
      if option.text == "CR-V":
        choosable_options.append(option)
    choosen_model = random.choice(choosable_options)
    choosen_model.click()

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
        if option.text == "2010":
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

    self.assertIn("Projeções Futuras", driver.page_source, "Projeções não carregadas")
    self.assertIn("stDataFrame", driver.page_source, "Tabela não carregada")
    self.assertIn("stImage", driver.page_source, "Gráfico não carregado")

  def tear_down(self):
    self.driver.quit()
    self.process.terminate()
  
if __name__ == "__main__":
  unittest.main()
