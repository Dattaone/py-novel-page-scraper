from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait
import requests
import os
import time

url = "https://translate.google.com/?hl=es&sl=en&tl=es&op=docs"


file_path = "translated_text.txt"

absolute_path = os.path.abspath(file_path)

def main():
    service = Service(ChromeDriverManager().install())
    option = webdriver.ChromeOptions()

    option.add_argument("--window-size=1920, 1080")
    driver = Chrome(service = service, options = option)
    driver.get(url)
    time.sleep(5)  # Espera que la página cargue

    # Encontrar y enviar el archivo
    file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    file_input.send_keys(absolute_path)
    
    # Espera opcional para que el archivo se cargue
    time.sleep(2)

    # Hacer clic en el botón (Explorar archivos)
    button = driver.find_element(By.XPATH, "//span[text()='Explorar archivos']")
    button.click()

    time.sleep(15)


if __name__ == "__main__":
    main()
