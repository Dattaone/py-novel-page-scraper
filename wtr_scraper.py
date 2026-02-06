from base_scraper import BaseScraper
from selenium.webdriver.common.by import By
import logging
import math
import random

class WtrScraper(BaseScraper):
    def scrape_last_chapter(self):
        try:
            div_element = self.get_elements(By.CSS_SELECTOR, "div table a")
            links = [a.get_attribute("href") for a in div_element]
            logging.info("Ültimo capítulo extraido")
            return links[0]
        except Exception as e:
            logging.error(f"Error al extraer la lista: {e}")
            return []
        

    def scrape_chapter(self, number_chapter: int, max_retries=5):
        for attempt in range(1, max_retries + 1):
            try:
                self.wait_random(0.8, 1.3)
                
                div_element = self.get_element(By.ID, f"chapter-{number_chapter}")
                text = div_element.text.strip()

                if text:
                    logging.info(f"Capítulo {number_chapter} extraído")
                    return self.formated_text(text)

                logging.warning(
                    f"❗ Capítulo {number_chapter} vacío (intento {attempt}/{max_retries})"
                )

                self.human_scroll_to_element()

            except Exception as e:
                logging.error(
                    f"❌ Error en capítulo {number_chapter} (intento {attempt}/{max_retries}): {e}"
                )
                self.wait_random(0.8, 1.3)

        # Si falló 5 veces:
        logging.error(f"🚨 No se pudo extraer el capítulo {number_chapter} después de {max_retries} intentos")
        return ""  # evitar que rompa el scrape entero



    def scrape(self, url, start=None, end=None):
        max_retries = 3
        attempt = 1
        current_chapter = 1  # capítulo actual
        
        while attempt <= max_retries:
            try:
                logging.info(f"Intento {attempt}/{max_retries}...")
                self.start_driver()
                self.driver.get(url)

                # Se obtiene el último capítulo solo una vez
                if attempt == 1:
                    last_url = self.scrape_last_chapter()
                    base_url = self.tp.get_base_url(url)

                # Continuar desde donde quedó
                i = current_chapter

                while True:
                    chapter_url = f"{base_url}/chapter-{i}?service=web"
                    
                    self.driver.get(chapter_url)
                    text = self.scrape_chapter(i)


                    self.novel_text += text
                    self.novel_text += "\n\n\n"

                    # Si llegamos al final, terminamos todo
                    if f"{base_url}/chapter-{i}" == last_url:
                        self.close_driver()
                        return self.novel_text

                    
                    i += 1  # próximo capítulo
                    current_chapter = i  # guardamos progreso

            except Exception as e:
                logging.error(f"❌ Error en intento {attempt}: {e}")
                self.close_driver()
                self.wait_random()

            else:
                break

        logging.error("🚨 Se agotaron los 3 intentos de reintento.")
        return self.novel_text
    

        
    def human_scroll_to_element(self, steps_range=(15, 40)):
        current_y = self.driver.execute_script("return window.scrollY || window.pageYOffset;")
        target_y = self.driver.execute_script("return document.body.scrollHeight;")

        distance = target_y - current_y

        if distance == 0:
            return
        
        steps = random.randint(*steps_range)

        for i in range(1, steps+1):
            t = i/steps
            ease = 1 - (1 -t) * (1 - t)
            y = current_y + distance * ease
            self.driver.execute_script(f"window.scrollTo(0, {math.floor(y)});")
            self.wait_random(0.91,0.96)

        self.driver.execute_script(f"window.scrollTo(0, {target_y});")
        self.wait_random(0.1, 0.4)


    def formated_text(self, text):
        if not text:
            logging.warning("No se obtuvo texto en este capítulo.")
            return ""
        lines = text.splitlines()
        
        if len(lines) > 2:
            lines.pop(2)
            lines[1]= ""
        
        text = "\n".join(lines)

        return text    


    

    

        
