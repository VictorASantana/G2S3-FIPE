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

  def test_user_not_logged(self):
    driver = self.driver
    wait = WebDriverWait(driver, 10)

    price_search_button = wait.until(
      EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Consultar preços')]"))
    )

    price_search_button.click()

    time.sleep(3)

    history_tab = wait.until(
      EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Minhas consultas')]"))
    )

    history_tab.click()

    time.sleep(4)

    self.assertIn("Você precisa estar logado para visualizar suas consultas salvas.", driver.page_source, "Alerta não emitido")

  def tear_down(self):
    self.driver.quit()
    self.process.terminate()
  
if __name__ == "__main__":
  unittest.main()
