from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options

import undetected_chromedriver as uc

import os
import time
import glob


class GoogleTranslateScraper:
    def __init__(self):
        """Inicializa el scraper y configura el navegador."""
        self.url = "https://translate.google.com/?hl=es&sl=zh-CN&tl=es&text=%E7%A8%8D%E5%90%8E%E5%86%8D%E8%AF%95&op=docs"
        """ self.url = "https://translate.google.com/?sl=en&tl=es&op=docs" """
        self.driver = None

    def start_driver(self, file_path):
        """Inicia el navegador."""
        # Define la ruta absoluta a tu carpeta deseada
        download_path = os.path.abspath(os.path.dirname(file_path))

        options = uc.ChromeOptions()
        #options.add_argument("--headless=new")
        options.add_argument("--window-size=800,600")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        prefs = {
            "download.default_directory": download_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }

        options.add_experimental_option("prefs", prefs)

        self.driver = uc.Chrome(version_main=140, options = options)
        self.driver.get(self.url)
        time.sleep(5)
    
    def get_download_file_dir(self, download_path, extension=".docx", timeout=80):
        old_files = set(os.listdir(download_path))
        initial_time = time.time()
        while time.time() - initial_time < timeout:
            actually_files = set(os.listdir(download_path))
            new_files = actually_files - old_files
            for new_file in new_files:
                if new_file.endswith(extension) and not new_file.endswith(".crdownload"):
                    end_path = os.path.join(download_path, new_file)
                    while not os.path.exists(end_path) or new_file.endswith(".crdownload"):
                        time.sleep(0.5)
                    return end_path
            time.sleep(1)
        raise TimeoutError("No se detecto en el tiempo limite")

    def translate_file(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"El archivo '{file_path}' no  existe.")

        absolute_path = os.path.abspath(file_path)



        """ 
        # Simula movimiento del mouse y scroll
        self.driver.execute_script("window.scrollTo(0, 300);")
        self.driver.execute_script("document.querySelector('body').dispatchEvent(new Event('mousemove'));")
        time.sleep(2) """

        
    
        file_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='file']")
        file_input.send_keys(absolute_path)

        print("Archivo cargado. Clikear botón 'Traducir'...")
        
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Traducir']"))
        ).click()

        print("Esperando que se procese la traducción...")
        # Espera a que el texto traducido esté presente o cambie el botón
        """ 
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//span[text()='Descargar traducción']"))
        ) 
        """

        time.sleep(25)  

        print("Descargando archivo traducido...")
        WebDriverWait(self.driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Descargar traducción']"))
        ).click()

        download_dir = os.path.dirname(os.path.abspath(file_path))
        download_file_path = self.get_download_file_dir(download_dir)

        final_path = os.path.join(download_dir, os.path.basename(file_path))
        if os.path.exists(final_path):
            os.remove(final_path)
        os.rename(download_file_path, final_path)


        time.sleep(25)  # Espera para asegurar que se complete la descarga



    def close_driver(self):
        """Cierra el navegador."""
        if self.driver:
            self.driver.quit()

    def translate(self, file_path):
        """
        Traduce un archivo completo a través de Google Translate.
        
        :param file_path: Ruta del archivo a traducir.
        """
        try:
            self.start_driver(file_path)
            self.translate_file(file_path)
        finally:
            self.close_driver()


# Uso de la clase
if __name__ == "__main__":
    # Ruta del archivo que deseas traducir
    file_path = "23.docx"

    # Instancia de la clase y traducción del archivo
    translator = GoogleTranslateScraper()
    translator.translate(file_path)
