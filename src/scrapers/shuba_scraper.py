import logging
from selenium.webdriver.common.by import By
from src.scrapers.base_scraper import BaseScraper

class ShubaScraper(BaseScraper):
    """Scraper especializado para el sitio de Shuba."""

    def scrape_list_chapters(self):
        try:
            div_element = self.get_element(By.ID, "catalog")
            links = div_element.find_elements(By.CSS_SELECTOR, "ul li a")
            return [a.get_attribute("href") for a in links]
        except Exception as e:
            logging.error(f"Error al extraer la lista: {e}")
            return []


    def scrape_chapter(self):
        try:
            content = self.get_element(By.CSS_SELECTOR, ".txtnav", timeout=30).text.strip()
            return content
        except Exception as e:
            logging.error(f"Error al extraer capítulo(scrape_chapter) {e}")
            return ""


    def format_text(self, text):
        lines = text.splitlines()
        title = ""
        if len(lines) > 2:
            lines.pop(1)
            title = lines.pop(0)
        if not lines[0].startswith("第"):
            lines.insert(0, title)

        return "\n".join(lines)
    

    def log_chapter_extraction(self, text):
        title = self.tp.extract_line(text).strip()

        if not title.startswith("第"):
            title = self.tp.translate_text(target_language="es", source_language="zh-CN", text=title)
            logging.info(f"{title} extraído.")
        
        match = self.tp.search_number(title)

        if match:
            num = float(match.group(1))

            # Si el capítulo es decimal (ej. 第2.5章), mostrar el título literal
            if not num.is_integer():
                logging.info(f"{title} extraído.")

            # Capítulo normal (entero)
            logging.info(f"Capítulo {int(num)} extraído.")


    def scrape(self, url: str, start: int = 1, end = None):
        """
        Extrae capítulos de una novela desde una página web de índice.

        Este método inicia un navegador automatizado, obtiene la lista de capítulos
        de la novela indicada en la URL, y descarga el contenido de cada capítulo
        dentro del rango especificado (`start` → `end`).

        Args:
            url (str): URL del índice de la novela (página que contiene los enlaces a los capítulos).
            start (int, opcional): Número del primer capítulo a descargar. 
                Por defecto, 1 (el primer capítulo).
            end (int, opcional): Número del último capítulo a descargar. 
                Si no se especifica (`None`), se descargan todos los capítulos disponibles.

        Returns:
            str: Texto completo con todos los capítulos extraídos y formateados,
                concatenados en una sola cadena.

        """
        try:
            self.start_driver()
            self.driver.get(url)

            chapters = self.scrape_list_chapters()

            # Si no se indica "end", tomamos todos los capitulos
            if end is None:
                end = len(chapters)
            if start is None:
                start = 1


            for _, link in enumerate(chapters[start-1:end], start):
                self.driver.get(link)
                self.wait_random(1.5,3.5)

                text = self.scrape_chapter()
                text = self.format_text(text)
                self.novel_text += text + "\n\n"

                self.log_chapter_extraction(text)

        except Exception as e:
            logging.error(f"Error general en scrape: {e}")
        finally:
            self.close_driver()
            return self.novel_text
