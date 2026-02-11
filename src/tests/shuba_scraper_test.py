import time
import random
import logging

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from text_processor import TextProcessor
from src.ui.keyboard_interface import KeyboardInterface

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class ShubaScraper:
    def __init__(self):
        """Inicializa el scraper y configura el navegador."""
        self.driver = None
        
    
    def start_driver(self):
        """Inicia el navegador."""
        # Define la ruta absoluta a tu carpeta deseada

        options = uc.ChromeOptions()
        #options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        options.add_argument("--disable-setuid-sandbox")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-application-cache")

        self.driver = uc.Chrome(options = options)
        
    
    def close_driver(self):
        """ Cierre delnavegador """
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass
            self.driver.__del__ = lambda: None  # evita WinError 6

    def scrape_list_chapters(self):
        try:

            div_element = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.ID, "catalog"))
            )

            links = div_element.find_elements(By.CSS_SELECTOR, "ul li a")


            urls = [a.get_attribute("href") for a in links]
            

            return urls
        except Exception as e:
            logging.error(f"Error al extraer la lista: {e}")


    def scrape_chapter(self):
        try:
            content = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".txtnav"))
            ).text.strip()

            return content

        except Exception as e:
            logging.error(f"Error al extraer capítulo: {e}")
            return ""

    def scrape_novel(self, url:str):
        try:
            self.start_driver()
            self.driver.get(url)

            chapter_links = self.scrape_list_chapters()

            all_novel = ""

            for i, chapter_link in enumerate(chapter_links):
                time.sleep(random.uniform(1, 3))
                self.driver.get(chapter_link)

                text_chapter = self.scrape_chapter()
                text_chapter = self.format_text(text_chapter)
                all_novel += text_chapter
                all_novel += "\n\n"
                logging.info(f"Capítulo {i+1} extraido exitosamente. ")

                
        except Exception as e:
            logging.error(f"Error de extraccion del capítulo : {e}")
        finally:
            self.close_driver()
            return all_novel



    def format_text(self, text):
        if not text:
            logging.warning("No se obtuvo texto en este capítulo.")
            return ""
        lines = text.splitlines()
        
        if len(lines) > 2:
            lines.pop(1)
            lines.pop(0)
        
        text = "\n".join(lines)

        return text    



def main():
    scraper = ShubaScraper()
    ki = KeyboardInterface()
    ki.clear()
    url = ki.get_input_url()
    if url.endswith(".html") or url.endswith(".htm"):
        url = url.rsplit(".", 1)[0] + "/"

    filename = ki.get_input_filename()
    novel = scraper.scrape_novel(url)
    tp = TextProcessor()
    tp.create_docx_from_text(novel, f"{filename}.docx")
    

# Uso de la clase
if __name__ == "__main__":
    # Instancia de la clase y traducción del archivo
    main()



        

